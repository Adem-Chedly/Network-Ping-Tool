# 🌐 Network Ping Tool

A cross-platform command-line utility for testing network connectivity, measuring latency, and logging results. Built with Python's subprocess module for real system interaction.

## ✨ Features

### 🎯 Core Functionality
- **Ping any host**: IP addresses or domain names
- **Latency measurement**: Min, max, and average response times
- **Packet loss detection**: Track connection reliability
- **Individual response times**: See each ping result
- **Cross-platform**: Works on Windows, Linux, and macOS

### 📊 Advanced Features
- **Input validation**: IP and domain name verification
- **Result parsing**: Extract statistics from ping output
- **Log management**: Save and view ping history
- **Quick ping**: Instant connectivity test
- **Colored feedback**: Visual latency indicators
- **Customizable**: Configure ping count

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- Network connectivity (obviously! 😄)
- No external dependencies required

### Installation

1. Download the project:
   ```bash
   cd ping-tool
   ```

2. Make executable (optional, Linux/Mac):
   ```bash
   chmod +x ping.py
   ```

### Usage

Run the tool:
```bash
python ping.py
```

Or directly (if executable):
```bash
./ping.py
```

## 📚 How to Use

### Interactive Menu

```
==================================================
🌐 NETWORK PING TOOL
==================================================

Options:
  1. Ping a host
  2. Quick ping (google.com)
  3. View logs
  4. Clear logs
  5. Exit
==================================================
```

### Example Session

```bash
Enter your choice (1-5): 1

Enter IP address or domain: google.com
Number of pings (default 4): 4

============================================================
🌐 Pinging google.com (domain)...
============================================================

✅ Ping Successful!

📊 Statistics for google.com:
------------------------------------------------------------
  Packets Sent:     4
  Packets Received: 4
  Packet Loss:      0.0%

⏱️  Latency:
------------------------------------------------------------
  Minimum:  15.34 ms
  Average:  18.76 ms
  Maximum:  23.45 ms

📈 Individual Response Times:
------------------------------------------------------------
  Reply 1: 🟢 15.34 ms
  Reply 2: 🟢 18.23 ms
  Reply 3: 🟢 19.87 ms
  Reply 4: 🟢 23.45 ms
============================================================

Save to log file? (y/n): y
✅ Results saved to logs.txt
```

## 🔧 Technical Details

### Architecture

```
ping.py
├── PingTool (Class)
│   ├── validate_target()      # Validate IP/domain
│   ├── build_ping_command()   # Platform-specific command
│   ├── ping()                 # Execute ping
│   ├── parse_ping_output()    # Extract statistics
│   ├── display_results()      # Format output
│   ├── log_results()          # Save to file
│   ├── view_logs()            # Display history
│   └── clear_logs()           # Clear history
└── main()                     # Application loop
```

### How It Works

1. **Input Validation**: Validates IP addresses and domain names using regex
2. **Command Building**: Creates platform-specific ping commands
3. **Execution**: Uses `subprocess.run()` to execute system ping
4. **Parsing**: Extracts statistics using regex patterns
5. **Display**: Formats results with colored indicators
6. **Logging**: Appends results to text file

### Platform Differences

**Windows:**
```bash
ping -n 4 google.com
```

**Linux/Mac:**
```bash
ping -c 4 google.com
```

The tool automatically detects your OS and uses the correct format!

### Input Validation

**Valid IP addresses:**
- `192.168.1.1`
- `8.8.8.8`
- `10.0.0.1`

**Valid domains:**
- `google.com`
- `github.com`
- `localhost`
- `api.example.com`

**Invalid inputs:**
- `999.999.999.999` (out of range)
- `not a domain` (invalid format)
- `192.168.1` (incomplete IP)

### Latency Indicators

Response times are color-coded:
- 🟢 **< 50ms**: Excellent (green)
- 🟡 **50-150ms**: Good (yellow)
- 🔴 **> 150ms**: Slow (red)

## 📄 Log File Format

The `logs.txt` file stores results in this format:

```
============================================================
Timestamp: 2024-12-16 14:30:25
Target: google.com
Type: domain
Success: True
Packets Sent: 4
Packets Received: 4
Packet Loss: 0.0%
Avg Latency: 18.76 ms
Min Latency: 15.34 ms
Max Latency: 23.45 ms
============================================================
```

## 🎯 Learning Outcomes

This project teaches:

- ✅ **Subprocess Management**: Execute system commands from Python
- ✅ **Output Parsing**: Extract data using regex
- ✅ **Cross-Platform Development**: Handle OS differences
- ✅ **File I/O**: Read and write log files
- ✅ **Networking Basics**: Understanding ping, latency, packet loss
- ✅ **Error Handling**: Timeouts, invalid input, parsing errors
- ✅ **Data Validation**: Input sanitization and verification

## 🧪 Testing Examples

### Test Local Network
```bash
ping 192.168.1.1      # Your router
ping localhost        # Your machine
```

### Test Internet
```bash
ping google.com       # Google DNS
ping 8.8.8.8         # Google Public DNS
ping github.com      # GitHub servers
```

### Test Latency
```bash
ping 1.1.1.1         # Cloudflare (usually fast)
ping aws.amazon.com  # AWS (varies by location)
```

## 📊 Understanding Results

### Packet Loss
- **0%**: Perfect connection
- **1-10%**: Some issues, usually acceptable
- **10-30%**: Poor connection
- **>30%**: Severe problems

### Latency
- **<20ms**: Excellent (gaming, real-time)
- **20-50ms**: Very good (most uses)
- **50-150ms**: Good (browsing, streaming)
- **>150ms**: Noticeable delay

### What Affects Ping?
- Distance to server
- Network congestion
- ISP routing
- Wireless vs wired
- Server load

## 🚀 Extension Ideas

### Easy
- [ ] Add continuous ping mode (until stopped)
- [ ] Export logs to CSV
- [ ] Ping multiple hosts in sequence
- [ ] Add timestamp to each ping reply

### Medium
- [ ] Traceroute functionality
- [ ] Graphical latency chart (ASCII art)
- [ ] Alert on connection loss
- [ ] Compare multiple hosts side-by-side
- [ ] Schedule periodic pings

### Advanced
- [ ] GUI with tkinter/PyQt
- [ ] Real-time monitoring dashboard
- [ ] Network diagnostic suite
- [ ] Historical trends and graphs
- [ ] Alert notifications (email/SMS)
- [ ] Integration with network monitoring tools

## ⚠️ Troubleshooting

### "Permission denied" on Linux/Mac
Some systems require sudo for ping:
```bash
sudo python ping.py
```

Or configure ping capabilities:
```bash
sudo setcap cap_net_raw+ep /usr/bin/ping
```

### Firewall blocking pings
- Windows: Allow ICMP in Windows Firewall
- Linux: `sudo ufw allow icmp`
- Router: Enable ICMP/ping responses

### "Host unreachable"
- Check target spelling
- Verify internet connection
- Try IP address instead of domain
- Check DNS settings

## 🔒 Security Considerations

- **ICMP flooding**: Don't use for DOS attacks
- **Privacy**: Pinging reveals your IP to target
- **Firewalls**: Some networks block ICMP
- **Logs**: May contain sensitive IPs

## 📝 License

Educational project - free to use and modify!

## 🤝 Contributing

Suggestions welcome! This is a learning project.

---

**Happy Pinging! 🌐📡**

### Quick Reference

**Common Targets:**
```
8.8.8.8           - Google DNS
1.1.1.1           - Cloudflare DNS
google.com        - Google
github.com        - GitHub
localhost         - Your machine
192.168.1.1       - Typical router
```

**Quick Commands:**
```python
# In Python scripts
from ping import PingTool

tool = PingTool()
results = tool.ping("google.com", count=4)
print(f"Average: {results['avg_time']}ms")
```
