#!/usr/bin/env python3
import socket
import sys
import time

def main():
    host = 'data.adsbhub.org'
    port = 5002
    
    print(f"Connecting to {host}:{port}...")
    
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for connection attempt (optional)
        sock.settimeout(10)
        sock.connect((host, port))
        print(f"Connected to {host}:{port}")
        # Reset timeout for receiving data (optional)
        sock.settimeout(None)
        
        while True:
            try:
                # Receive data in chunks of 4096 bytes
                data = sock.recv(4096)
                if not data:
                    print("Connection closed by server")
                    break
                # Write raw bytes to stdout
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print("\nInterrupted by user")
                break
            except Exception as e:
                print(f"Error receiving data: {e}")
                break
                
    except socket.timeout:
        print("Connection timeout")
    except ConnectionRefusedError:
        print("Connection refused - check host and port")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        print("Socket closed")

if __name__ == "__main__":
    main()
