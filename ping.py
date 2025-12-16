#!/usr/bin/env python3
"""
Network Ping Tool
A cross-platform utility for testing network connectivity and latency
"""

import subprocess
import platform
import re
import os
from datetime import datetime


class PingTool:
    """Network ping utility with result parsing and logging"""
    
    def __init__(self, log_file="logs.txt"):
        self.log_file = log_file
        self.system = platform.system().lower()
        
    def validate_target(self, target):
        """Validate IP address or domain name"""
        # Basic validation for IP or domain
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        domain_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        
        if re.match(ip_pattern, target):
            # Validate IP range (0-255)
            octets = target.split('.')
            if all(0 <= int(octet) <= 255 for octet in octets):
                return True, "ip"
        elif re.match(domain_pattern, target) or target == "localhost":
            return True, "domain"
        
        return False, None
    
    def build_ping_command(self, target, count=4):
        """Build platform-specific ping command"""
        if self.system == "windows":
            # Windows: ping -n <count> <target>
            return ["ping", "-n", str(count), target]
        else:
            # Linux/Mac: ping -c <count> <target>
            return ["ping", "-c", str(count), target]
    
    def parse_ping_output(self, output):
        """Parse ping command output and extract statistics"""
        results = {
            "packets_sent": 0,
            "packets_received": 0,
            "packet_loss": 0.0,
            "min_time": None,
            "avg_time": None,
            "max_time": None,
            "times": [],
            "success": False
        }
        
        try:
            lines = output.split('\n')
            
            # Extract individual ping times
            if self.system == "windows":
                time_pattern = r'time[=<](\d+)ms'
            else:
                time_pattern = r'time=(\d+\.?\d*)\s*ms'
            
            for line in lines:
                match = re.search(time_pattern, line, re.IGNORECASE)
                if match:
                    time_ms = float(match.group(1))
                    results["times"].append(time_ms)
            
            # Extract packet statistics
            if self.system == "windows":
                # Windows format: "Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)"
                packets_match = re.search(r'Sent = (\d+), Received = (\d+), Lost = (\d+)', output)
                if packets_match:
                    results["packets_sent"] = int(packets_match.group(1))
                    results["packets_received"] = int(packets_match.group(2))
                    lost = int(packets_match.group(3))
                    if results["packets_sent"] > 0:
                        results["packet_loss"] = (lost / results["packets_sent"]) * 100
                
                # Windows time stats: "Minimum = 1ms, Maximum = 4ms, Average = 2ms"
                stats_match = re.search(r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms', output)
                if stats_match:
                    results["min_time"] = float(stats_match.group(1))
                    results["max_time"] = float(stats_match.group(2))
                    results["avg_time"] = float(stats_match.group(3))
            else:
                # Linux/Mac format: "4 packets transmitted, 4 received, 0% packet loss"
                packets_match = re.search(r'(\d+) packets transmitted, (\d+) received', output)
                if packets_match:
                    results["packets_sent"] = int(packets_match.group(1))
                    results["packets_received"] = int(packets_match.group(2))
                
                loss_match = re.search(r'(\d+\.?\d*)% packet loss', output)
                if loss_match:
                    results["packet_loss"] = float(loss_match.group(1))
                
                # Linux/Mac time stats: "rtt min/avg/max/mdev = 1.234/2.345/3.456/0.567 ms"
                stats_match = re.search(r'rtt min/avg/max/[a-z]+ = ([\d.]+)/([\d.]+)/([\d.]+)', output)
                if stats_match:
                    results["min_time"] = float(stats_match.group(1))
                    results["avg_time"] = float(stats_match.group(2))
                    results["max_time"] = float(stats_match.group(3))
            
            # If we got times manually, calculate stats if not found
            if results["times"] and not results["avg_time"]:
                results["min_time"] = min(results["times"])
                results["max_time"] = max(results["times"])
                results["avg_time"] = sum(results["times"]) / len(results["times"])
            
            # Mark as successful if we received any packets
            results["success"] = results["packets_received"] > 0
            
        except Exception as e:
            print(f"⚠️  Warning: Error parsing output - {e}")
        
        return results
    
    def ping(self, target, count=4, show_output=True):
        """Execute ping command and return results"""
        # Validate target
        is_valid, target_type = self.validate_target(target)
        if not is_valid:
            return {
                "success": False,
                "error": "Invalid IP address or domain name"
            }
        
        if show_output:
            print(f"\n{'=' * 60}")
            print(f"🌐 Pinging {target} ({target_type})...")
            print(f"{'=' * 60}\n")
        
        try:
            # Build and execute ping command
            command = self.build_ping_command(target, count)
            
            # Run ping command
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            
            # Parse output
            output = result.stdout
            parsed_results = self.parse_ping_output(output)
            
            # Add metadata
            parsed_results["target"] = target
            parsed_results["target_type"] = target_type
            parsed_results["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            parsed_results["raw_output"] = output
            
            return parsed_results
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Ping command timed out",
                "target": target
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "target": target
            }
    
    def display_results(self, results):
        """Display ping results in a formatted way"""
        if not results["success"]:
            print(f"\n❌ Ping Failed")
            if "error" in results:
                print(f"   Error: {results['error']}")
            print()
            return
        
        print(f"✅ Ping Successful!")
        print(f"\n📊 Statistics for {results['target']}:")
        print("-" * 60)
        print(f"  Packets Sent:     {results['packets_sent']}")
        print(f"  Packets Received: {results['packets_received']}")
        print(f"  Packet Loss:      {results['packet_loss']:.1f}%")
        
        if results['min_time'] is not None:
            print(f"\n⏱️  Latency:")
            print("-" * 60)
            print(f"  Minimum:  {results['min_time']:.2f} ms")
            print(f"  Average:  {results['avg_time']:.2f} ms")
            print(f"  Maximum:  {results['max_time']:.2f} ms")
        
        # Show individual times if available
        if results['times']:
            print(f"\n📈 Individual Response Times:")
            print("-" * 60)
            for i, time in enumerate(results['times'], 1):
                status = "🟢" if time < 50 else "🟡" if time < 150 else "🔴"
                print(f"  Reply {i}: {status} {time:.2f} ms")
        
        print("=" * 60 + "\n")
    
    def log_results(self, results):
        """Save ping results to log file"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"\n{'=' * 60}\n")
                f.write(f"Timestamp: {results.get('timestamp', 'N/A')}\n")
                f.write(f"Target: {results.get('target', 'N/A')}\n")
                f.write(f"Type: {results.get('target_type', 'N/A')}\n")
                f.write(f"Success: {results['success']}\n")
                
                if results['success']:
                    f.write(f"Packets Sent: {results['packets_sent']}\n")
                    f.write(f"Packets Received: {results['packets_received']}\n")
                    f.write(f"Packet Loss: {results['packet_loss']:.1f}%\n")
                    if results['avg_time']:
                        f.write(f"Avg Latency: {results['avg_time']:.2f} ms\n")
                        f.write(f"Min Latency: {results['min_time']:.2f} ms\n")
                        f.write(f"Max Latency: {results['max_time']:.2f} ms\n")
                else:
                    f.write(f"Error: {results.get('error', 'Unknown')}\n")
                
                f.write(f"{'=' * 60}\n")
            
            return True
        except Exception as e:
            print(f"⚠️  Warning: Could not write to log file - {e}")
            return False
    
    def view_logs(self):
        """Display recent log entries"""
        if not os.path.exists(self.log_file):
            print(f"\n📭 No log file found at '{self.log_file}'\n")
            return
        
        try:
            with open(self.log_file, 'r') as f:
                content = f.read()
            
            if not content.strip():
                print(f"\n📭 Log file is empty\n")
                return
            
            print(f"\n{'=' * 60}")
            print(f"📄 PING LOGS ({self.log_file})")
            print(f"{'=' * 60}")
            print(content)
            
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
    
    def clear_logs(self):
        """Clear the log file"""
        try:
            with open(self.log_file, 'w') as f:
                f.write(f"# Ping Tool Logs - Cleared on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"✅ Logs cleared successfully!\n")
        except Exception as e:
            print(f"❌ Error clearing logs: {e}\n")


def show_menu():
    """Display main menu"""
    print("\n" + "=" * 60)
    print("🌐 NETWORK PING TOOL")
    print("=" * 60)
    print("\nOptions:")
    print("  1. Ping a host")
    print("  2. Quick ping (google.com)")
    print("  3. View logs")
    print("  4. Clear logs")
    print("  5. Exit")
    print("=" * 60)


def main():
    """Main application loop"""
    tool = PingTool()
    
    print("\n🚀 Welcome to Network Ping Tool!")
    print("Test network connectivity and latency.\n")
    
    while True:
        show_menu()
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            target = input("\nEnter IP address or domain: ").strip()
            if not target:
                print("❌ No target entered.")
                continue
            
            try:
                count = int(input("Number of pings (default 4): ").strip() or "4")
                if count < 1 or count > 100:
                    print("⚠️  Using default count of 4 (range: 1-100)")
                    count = 4
            except ValueError:
                print("⚠️  Invalid number, using default count of 4")
                count = 4
            
            results = tool.ping(target, count)
            tool.display_results(results)
            
            # Ask to save
            save = input("Save to log file? (y/n): ").lower()
            if save == 'y':
                if tool.log_results(results):
                    print(f"✅ Results saved to {tool.log_file}\n")
        
        elif choice == "2":
            print("\n🔍 Quick ping to google.com...")
            results = tool.ping("google.com", 4)
            tool.display_results(results)
            tool.log_results(results)
            print(f"📝 Results logged to {tool.log_file}\n")
        
        elif choice == "3":
            tool.view_logs()
        
        elif choice == "4":
            confirm = input("Are you sure you want to clear all logs? (y/n): ").lower()
            if confirm == 'y':
                tool.clear_logs()
        
        elif choice == "5":
            print("\n👋 Thanks for using Network Ping Tool!")
            print("Stay connected! 🌐\n")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
