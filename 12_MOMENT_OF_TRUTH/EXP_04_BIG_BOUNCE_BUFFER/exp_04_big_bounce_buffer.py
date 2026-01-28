import time
import random
import sys
import hashlib
import matplotlib.pyplot as plt
import collections

# --- CONFIGURATION ---
BUFFER_CAPACITY = 1000  # Virtual Units (MB or whatever)
INCOMING_RATE = 100     # Requests per second
PROCESSING_RATE = 20    # Requests per second (Server is overloaded 5x)
SIM_DURATION = 5.0      # Seconds

class Request:
    def __init__(self, req_id, data_size=10):
        self.id = req_id
        self.data_size = data_size
        self.content = "DATA_" * data_size # Simulated content
        self.resolution = 1.0 # 100% Quality
        self.timestamp = time.time()
        
    def compress(self):
        """Holographic Compression: Reduce size and resolution."""
        if self.resolution <= 0.1:
            return False # Cannot compress further
        
        # Simulate compression by hashing content
        # We reduce size by half each step
        self.resolution /= 2.0
        self.data_size = max(1, int(self.data_size / 2))
        return True

class StandardServer:
    def __init__(self):
        self.buffer = collections.deque()
        self.current_load = 0
        self.dropped_packets = 0
        self.processed_packets = 0
        self.crashed = False
        
    def enqueue(self, req):
        if self.crashed: return
        
        if self.current_load + req.data_size <= BUFFER_CAPACITY:
            self.buffer.append(req)
            self.current_load += req.data_size
        else:
            self.dropped_packets += 1
            # In a real severe overflow, this might crash OS pointers
            if self.dropped_packets > 200: 
                self.crashed = True
                
    def process(self):
        if self.crashed: return
        if self.buffer:
            req = self.buffer.popleft()
            self.current_load -= req.data_size
            self.processed_packets += 1

class TamesisServer:
    def __init__(self):
        self.buffer = collections.deque() # Queue of Requests
        self.current_load = 0
        self.dropped_packets = 0
        self.processed_packets = 0
        self.compression_events = 0
        
    def enqueue(self, req):
        # --- BIG BOUNCE LOGIC ---
        # 1. Check Capacity
        while self.current_load + req.data_size > BUFFER_CAPACITY:
            # 2. Entropic Backpressure
            # We don't drop the new packet. We squeeze the OLD packets.
            # "Space Repels Energy" -> "Full Buffer Repels Storage Size"
            
            # Find the oldest high-res packet to compress
            compressed_something = False
            for old_req in self.buffer:
                if old_req.resolution > 0.1:
                    load_before = old_req.data_size
                    if old_req.compress():
                        load_after = old_req.data_size
                        self.current_load -= (load_before - load_after)
                        self.compression_events += 1
                        compressed_something = True
                        if self.current_load + req.data_size <= BUFFER_CAPACITY:
                            break
            
            if not compressed_something:
                # Buffer is full of completely compressed dust.
                # Now we must drop (Event Horizon Reached).
                self.dropped_packets += 1
                return 

        # 3. Accept
        self.buffer.append(req)
        self.current_load += req.data_size

    def process(self):
        if self.buffer:
            req = self.buffer.popleft()
            self.current_load -= req.data_size
            self.processed_packets += 1

def run_experiment():
    print("--- TAMESIS EXPERIMENT 04: BIG BOUNCE BUFFER ---")
    print(f"Goal: Survive 500% Load ({INCOMING_RATE}/{PROCESSING_RATE}) without crashing.")
    
    std_server = StandardServer()
    tam_server = TamesisServer()
    
    ticks = int(SIM_DURATION * 10) # 10 ticks per second
    
    std_history = []
    tam_history = []
    
    req_counter = 0
    
    print("\nStarting Simulation...")
    for t in range(ticks):
        # Incoming Traffic Burst
        burst = int(INCOMING_RATE / 10)
        for _ in range(burst):
            req_counter += 1
            req = Request(req_counter)
            
            # Copy for fair test
            req_std = Request(req_counter)
            req_tam = Request(req_counter)
            
            std_server.enqueue(req_std)
            tam_server.enqueue(req_tam)
            
        # Processing Tick
        proc = int(PROCESSING_RATE / 10)
        for _ in range(proc):
            std_server.process()
            tam_server.process()
            
        # Log status
        std_history.append(std_server.current_load)
        tam_history.append(tam_server.current_load)
        
        if t % 10 == 0:
            print(f"Time {t/10:.1f}s | STD Dropped: {std_server.dropped_packets} (Crashed: {std_server.crashed}) | TAM Compr: {tam_server.compression_events} | TAM Dropped: {tam_server.dropped_packets}")

    print("\n--- RESULTS ---")
    print(f"STANDARD SERVER:")
    print(f"Processed: {std_server.processed_packets}")
    print(f"Dropped:   {std_server.dropped_packets}")
    print(f"Crashed:   {std_server.crashed}")
    
    print(f"\nTAMESIS SERVER:")
    print(f"Processed: {tam_server.processed_packets}")
    print(f"Dropped:   {tam_server.dropped_packets}")
    print(f"Compressed:{tam_server.compression_events} (Holographic Events)")
    
    # Visualization Code for Plots
    plt.figure(figsize=(10, 5))
    plt.plot(std_history, 'r--', label='Standard (Rigid)')
    plt.plot(tam_history, 'b-', label='Tamesis (Bounce/Elastic)')
    plt.axhline(y=BUFFER_CAPACITY, color='k', linestyle=':', label='Max Capacity')
    plt.title("Buffer Saturation: Rigid vs Elastic")
    plt.xlabel("Time (ticks)")
    plt.ylabel("Buffer Load")
    plt.legend()
    plt.savefig("bounce_buffer_result.png")
    print("Plot saved to bounce_buffer_result.png")

    if tam_server.dropped_packets < std_server.dropped_packets and not tam_server.dropped_packets == 0:
         print("\nPARTIAL SUCCESS: Tamesis dropped fewer packets, but still saturated.")
    elif tam_server.dropped_packets == 0:
         print("\nSPECTACULAR SUCCESS: Tamesis Server survived 500% load with ZERO LOSS.")
         print("It traded resolution for existence. The Big Bounce works.")
    else:
         print("\nFAILURE: Tamesis performed no better.")

if __name__ == "__main__":
    run_experiment()
