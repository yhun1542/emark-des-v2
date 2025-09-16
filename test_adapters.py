#!/usr/bin/env python3
import os
import sys
sys.path.append('./server')

# 환경 변수 설정
os.environ['ENABLE_REAL_CALLS'] = 'true'

print("=== Testing Adapter Imports ===")

try:
    from server.adapters_shim import get_providers
    print("Successfully imported get_providers")
    
    providers = get_providers()
    print(f"Created {len(providers)} providers")
    
    for i, provider in enumerate(providers):
        print(f"Provider {i}: {provider.key}, has_adapter: {provider.ad is not None}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

