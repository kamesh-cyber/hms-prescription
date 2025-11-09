#!/usr/bin/env python3
"""
Test script for verifying correlation ID functionality
"""

import requests
import uuid

BASE_URL = "http://localhost:8000"


def test_correlation_id():
    """Test correlation ID functionality"""

    print("="*60)
    print("Testing Correlation ID Functionality")
    print("="*60)

    # Test 1: Server generates correlation ID
    print("\n1. Testing server-generated correlation ID...")
    response = requests.get(f"{BASE_URL}/health")
    correlation_id = response.headers.get('X-Correlation-ID')

    if correlation_id:
        print(f"   ✓ Server generated correlation ID: {correlation_id}")
    else:
        print("   ✗ No correlation ID in response")

    # Test 2: Client provides correlation ID
    print("\n2. Testing client-provided correlation ID...")
    custom_id = f"test-{uuid.uuid4()}"
    headers = {'X-Correlation-ID': custom_id}
    response = requests.get(f"{BASE_URL}/health", headers=headers)
    returned_id = response.headers.get('X-Correlation-ID')

    if returned_id == custom_id:
        print(f"   ✓ Server preserved correlation ID: {returned_id}")
    else:
        print(f"   ✗ Expected: {custom_id}, Got: {returned_id}")

    # Test 3: X-Request-ID header
    print("\n3. Testing X-Request-ID header...")
    custom_id = f"req-{uuid.uuid4()}"
    headers = {'X-Request-ID': custom_id}
    response = requests.get(f"{BASE_URL}/health", headers=headers)
    returned_id = response.headers.get('X-Correlation-ID')

    if returned_id == custom_id:
        print(f"   ✓ Server accepted X-Request-ID: {returned_id}")
    else:
        print(f"   ✗ Expected: {custom_id}, Got: {returned_id}")

    # Test 4: API endpoint with correlation ID
    print("\n4. Testing API endpoint with correlation ID...")
    custom_id = f"api-test-{uuid.uuid4()}"
    headers = {'X-Correlation-ID': custom_id}
    response = requests.get(f"{BASE_URL}/api/v1/prescriptions/", headers=headers)
    returned_id = response.headers.get('X-Correlation-ID')

    if returned_id == custom_id and response.status_code == 200:
        print(f"   ✓ API endpoint preserved correlation ID: {returned_id}")
        print(f"   ✓ Status code: {response.status_code}")
    else:
        print(f"   ✗ Expected: {custom_id}, Got: {returned_id}")
        print(f"   ✗ Status code: {response.status_code}")

    # Test 5: POST request with correlation ID
    print("\n5. Testing POST request with correlation ID...")
    custom_id = f"post-{uuid.uuid4()}"
    headers = {
        'X-Correlation-ID': custom_id,
        'Content-Type': 'application/json'
    }
    payload = {
        "appointment_id": "TEST-APPT-999",
        "patient_id": 100,
        "doctor_id": 50,
        "medication": "Test Med",
        "dosage": "1-0-1",
        "days": 5
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/prescriptions/",
        json=payload,
        headers=headers
    )
    returned_id = response.headers.get('X-Correlation-ID')

    if returned_id == custom_id:
        print(f"   ✓ POST request preserved correlation ID: {returned_id}")
        print(f"   ✓ Status code: {response.status_code}")
    else:
        print(f"   ✗ Expected: {custom_id}, Got: {returned_id}")

    print("\n" + "="*60)
    print("Correlation ID Tests Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Check application logs: docker-compose logs app")
    print("2. Search for specific correlation ID:")
    print(f"   docker-compose logs app | grep '{custom_id}'")
    print("\n")


if __name__ == "__main__":
    try:
        test_correlation_id()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API")
        print("Make sure the service is running with: docker-compose up")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

