import unittest
import os
import importlib
import sys
import io
import contextlib
from test.TestUtils import TestUtils

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None
    except Exception:
        return None

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("ticket_tracking_system")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning the result or None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

def check_raises(func, args, expected_exception=Exception):
    """Check if a function raises an expected exception."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            func(*args)
        return False
    except expected_exception:
        return True
    except Exception:
        return False

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_invalid_input_handling(self):
        """Consolidated test for invalid input validation"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestInvalidInputHandling", False, "exception")
                print("TestInvalidInputHandling = Failed")
                return
                
            # Check if required functions exist
            required_functions = [
                'initialize_data',
                'add_ticket',
                'remove_ticket',
                'sort_tickets',
                'filter_tickets',
                'get_priority_tickets',
                'manage_queue',
                'update_ticket'
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
                    
            if missing_functions:
                self.test_obj.yakshaAssert("TestInvalidInputHandling", False, "exception")
                print("TestInvalidInputHandling = Failed")
                return
                
            # Get tickets for testing
            try:
                tickets_data = safely_call_function(self.module_obj, 'initialize_data')
                if not tickets_data or not isinstance(tickets_data, tuple) or len(tickets_data) < 1:
                    self.test_obj.yakshaAssert("TestInvalidInputHandling", False, "exception")
                    print("TestInvalidInputHandling = Failed")
                    return
                    
                tickets = tickets_data[0]
                if not tickets or not isinstance(tickets, list):
                    self.test_obj.yakshaAssert("TestInvalidInputHandling", False, "exception")
                    print("TestInvalidInputHandling = Failed")
                    return
            except Exception as e:
                self.test_obj.yakshaAssert("TestInvalidInputHandling", False, "exception")
                print("TestInvalidInputHandling = Failed")
                return
                
            all_errors = []
            active_queue = []
            
            # Test adding invalid ticket
            try:
                # Missing required fields
                invalid_ticket = {"id": "X999", "title": "Invalid"}
                
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'add_ticket')(tickets, invalid_ticket)):
                    all_errors.append("add_ticket() should raise ValueError for missing fields")
                    
                # Invalid ticket type
                invalid_ticket = {"id": "T999", "title": "Invalid", "type": "invalid_type", "priority": 2, "status": "new"}
                
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'add_ticket')(tickets, invalid_ticket)):
                    all_errors.append("add_ticket() should raise ValueError for invalid type")
                    
                # Invalid priority
                invalid_ticket = {"id": "T999", "title": "Invalid", "type": "technical", "priority": 10, "status": "new"}
                
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'add_ticket')(tickets, invalid_ticket)):
                    all_errors.append("add_ticket() should raise ValueError for invalid priority")
                    
                # Invalid status
                invalid_ticket = {"id": "T999", "title": "Invalid", "type": "technical", "priority": 2, "status": "invalid_status"}
                
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'add_ticket')(tickets, invalid_ticket)):
                    all_errors.append("add_ticket() should raise ValueError for invalid status")
            except Exception as e:
                all_errors.append(f"Error testing invalid ticket addition: {str(e)}")
                
            # Test out of range index for removing ticket
            try:
                if not check_raises(IndexError, lambda: getattr(self.module_obj, 'remove_ticket')(tickets, len(tickets) + 5)):
                    all_errors.append("remove_ticket() should raise IndexError for out of range index")
            except Exception as e:
                all_errors.append(f"Error testing out of range index for remove_ticket(): {str(e)}")
                
            # Test invalid sort key
            try:
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'sort_tickets')(tickets, "invalid_key")):
                    all_errors.append("sort_tickets() should raise ValueError for invalid key")
            except Exception as e:
                all_errors.append(f"Error testing invalid sort key: {str(e)}")
                
            # Test invalid filter type
            try:
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'filter_tickets')(tickets, "invalid_filter", "value")):
                    all_errors.append("filter_tickets() should raise ValueError for invalid filter type")
            except Exception as e:
                all_errors.append(f"Error testing invalid filter type: {str(e)}")
                
            # Test invalid priority level
            try:
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'get_priority_tickets')(tickets, 0)):
                    all_errors.append("get_priority_tickets() should raise ValueError for priority 0")
                    
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'get_priority_tickets')(tickets, 5)):
                    all_errors.append("get_priority_tickets() should raise ValueError for priority 5")
            except Exception as e:
                all_errors.append(f"Error testing invalid priority level: {str(e)}")
                
            # Test queue management with invalid operation
            try:
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'manage_queue')(tickets, active_queue, "invalid_operation")):
                    all_errors.append("manage_queue() should raise ValueError for invalid operation")
            except Exception as e:
                all_errors.append(f"Error testing invalid queue operation: {str(e)}")
                
            # Test queue with invalid index
            try:
                if not check_raises(IndexError, lambda: getattr(self.module_obj, 'manage_queue')(tickets, active_queue, "add", len(tickets) + 10)):
                    all_errors.append("manage_queue() should raise IndexError for out of range index")
            except Exception as e:
                all_errors.append(f"Error testing invalid queue index: {str(e)}")
                
            # Test queue size limit
            try:
                # Clear queue first
                safely_call_function(self.module_obj, 'manage_queue', tickets, active_queue, "clear")
                
                # First, fill the queue to max capacity
                for i in range(min(5, len(tickets))):
                    safely_call_function(self.module_obj, 'manage_queue', tickets, active_queue, "add", i)
                    
                # Then try to add one more ticket
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'manage_queue')(tickets, active_queue, "add", 0)):
                    all_errors.append("manage_queue() should raise ValueError when exceeding queue capacity")
                    
                # Clear queue for next tests
                safely_call_function(self.module_obj, 'manage_queue', tickets, active_queue, "clear")
            except Exception as e:
                all_errors.append(f"Error testing queue size limit: {str(e)}")
                
            # Test remove from queue with invalid index
            try:
                if not check_raises(IndexError, lambda: getattr(self.module_obj, 'manage_queue')(tickets, active_queue, "remove", 0)):
                    all_errors.append("manage_queue() should raise IndexError when removing from empty queue")
            except Exception as e:
                all_errors.append(f"Error testing remove from empty queue: {str(e)}")
                
            # Test update with invalid index
            try:
                if not check_raises(IndexError, lambda: getattr(self.module_obj, 'update_ticket')(tickets, len(tickets) + 5, "status", "resolved")):
                    all_errors.append("update_ticket() should raise IndexError for out of range index")
            except Exception as e:
                all_errors.append(f"Error testing update with invalid index: {str(e)}")
                
            # Test update with invalid status
            try:
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'update_ticket')(tickets, 0, "status", "invalid_status")):
                    all_errors.append("update_ticket() should raise ValueError for invalid status")
            except Exception as e:
                all_errors.append(f"Error testing update with invalid status: {str(e)}")
                
            # Test update with invalid priority
            try:
                if not check_raises(ValueError, lambda: getattr(self.module_obj, 'update_ticket')(tickets, 0, "priority", "10")):
                    all_errors.append("update_ticket() should raise ValueError for invalid priority")
            except Exception as e:
                all_errors.append(f"Error testing update with invalid priority: {str(e)}")
                
            if all_errors:
                self.test_obj.yakshaAssert("TestInvalidInputHandling", False, "exception")
                print("TestInvalidInputHandling = Failed")
            else:
                self.test_obj.yakshaAssert("TestInvalidInputHandling", True, "exception")
                print("TestInvalidInputHandling = Passed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestInvalidInputHandling", False, "exception")
            print("TestInvalidInputHandling = Failed")

if __name__ == '__main__':
    unittest.main()