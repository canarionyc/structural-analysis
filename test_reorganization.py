#!/usr/bin/env python3
"""
Test script to verify that all components of the reorganized pyStructuralAnalysis work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_autoimport():
    """Test the autoimport module functionality"""
    print("=== Testing autoimport module ===")
    
    try:
        from autoimport import import_all, create_structural_symbols
        print("✅ autoimport module imports successfully")
        
        # Test symbol creation
        symbols = create_structural_symbols()
        expected_symbols = ['x', 'y', 'z', 'L', 'a', 'b', 'h', 'E', 'G', 'nu', 'I', 'A', 'J', 'P', 'q', 'M', 'R_A', 'R_B', 'M_A', 'M_B']
        for sym in expected_symbols:
            assert sym in symbols, f"Missing symbol: {sym}"
        print("✅ All expected symbols created")
        
        # Test import_all function
        import_all()
        print("✅ import_all() executes without errors")
        
        return True
    except Exception as e:
        print(f"❌ autoimport test failed: {e}")
        return False

def test_scripts():
    """Test that scripts can be imported and run basic functionality"""
    print("\n=== Testing scripts ===")
    
    script_paths = [
        'examples/example.py',
        'scripts/euler_beam_analysis.py',
        'scripts/cantilever_analysis.py'
    ]
    
    success_count = 0
    for script_path in script_paths:
        try:
            print(f"Testing {script_path}...")
            # Test that the script can be imported without errors
            import subprocess
            result = subprocess.run([sys.executable, script_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ {script_path} runs successfully")
                success_count += 1
            else:
                print(f"❌ {script_path} failed with return code {result.returncode}")
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"❌ {script_path} test failed: {e}")
    
    return success_count == len(script_paths)

def test_symbolic_computation():
    """Test basic symbolic computation functionality"""
    print("\n=== Testing symbolic computation ===")
    
    try:
        from autoimport import import_all
        import_all()
        
        # Test basic symbolic operations
        expr1 = P * L**3 / (3 * E * I)
        expr2 = sp.integrate(x**2, x)
        expr3 = sp.diff(x**3, x)
        
        assert str(expr2) == "x**3/3", f"Integration test failed: {expr2}"
        assert str(expr3) == "3*x**2", f"Differentiation test failed: {expr3}"
        
        print("✅ Basic symbolic operations work")
        
        # Test with units
        test_length = 10 * ureg.meter
        test_force = 1000 * ureg.newton
        
        assert test_length.magnitude == 10, "Unit magnitude test failed"
        assert str(test_length.units) == "meter", "Unit type test failed"
        
        print("✅ Units functionality works")
        
        return True
    except Exception as e:
        print(f"❌ Symbolic computation test failed: {e}")
        return False

def test_directory_structure():
    """Test that the directory structure is as expected"""
    print("\n=== Testing directory structure ===")
    
    expected_dirs = ['scripts', 'examples', 'notebooks', 'docs', 'tests']
    expected_files = ['autoimport.py', 'requirements.txt', 'setup.py', 'README.md']
    
    missing_dirs = []
    missing_files = []
    
    for directory in expected_dirs:
        if not os.path.isdir(directory):
            missing_dirs.append(directory)
    
    for file in expected_files:
        if not os.path.isfile(file):
            missing_files.append(file)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ Directory structure is correct")
    return True

def main():
    """Run all tests"""
    print("Running pyStructuralAnalysis reorganization tests...\n")
    
    tests = [
        test_directory_structure,
        test_autoimport,
        test_symbolic_computation,
        test_scripts
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The reorganization is successful.")
        return 0
    else:
        print("💥 Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())