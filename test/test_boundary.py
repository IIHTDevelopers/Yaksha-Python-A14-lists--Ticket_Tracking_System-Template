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

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_boundary_scenarios(self):
        """Consolidated test for boundary scenarios"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return
            
            # Check if required functions exist
            required_functions = [
                'initialize_data',
                'add_ticket',
                'remove_ticket',
                'sort_tickets',
                'filter_tickets',
                'combine_queues',
                'get_priority_tickets',
                'manage_queue',
                'update_ticket'
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
                    
            if missing_functions:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return
                
            all_errors = []
            
            # Test with empty ticket list
            try:
                empty_tickets = []
                active_queue = []
                
                # Test queue limit
                tickets_data = safely_call_function(self.module_obj, 'initialize_data')
                if not tickets_data or not isinstance(tickets_data, tuple) or len(tickets_data) < 1:
                    all_errors.append("initialize_data() did not return proper data structure")
                else:
                    tickets = tickets_data[0]
                    
                    if not tickets or not isinstance(tickets, list):
                        all_errors.append("initialize_data() did not return a valid tickets list")
                    else:
                        # Try to fill queue to maximum capacity (5 tickets)
                        for i in range(min(5, len(tickets))):
                            try:
                                queue_result = safely_call_function(self.module_obj, 'manage_queue', tickets, active_queue, "add", i)
                                if queue_result is None:
                                    all_errors.append(f"manage_queue() returned None when adding ticket {i}")
                                    break
                            except Exception as e:
                                all_errors.append(f"Error adding ticket {i} to queue: {str(e)}")
                                break
                        
                        if len(active_queue) != min(5, len(tickets)):
                            all_errors.append(f"Queue should allow up to 5 tickets, got {len(active_queue)}")
            except Exception as e:
                all_errors.append(f"Error testing queue size limit: {str(e)}")
                
            # Test adding tickets to an empty list
            try:
                empty_tickets = []
                new_ticket = {"id": "T100", "title": "Test ticket", "type": "technical", "priority": 2, "status": "new"}
                
                result = safely_call_function(self.module_obj, 'add_ticket', empty_tickets, new_ticket)
                
                if result is None:
                    all_errors.append("add_ticket() returned None when adding to empty list")
                elif not isinstance(result, list):
                    all_errors.append(f"add_ticket() should return a list, got {type(result)}")
                elif len(result) != 1:
                    all_errors.append(f"Should be able to add ticket to empty list, got list of size {len(result)}")
                    
                # Test removing the only ticket
                if result and len(result) == 1:
                    removed = safely_call_function(self.module_obj, 'remove_ticket', result, 0)
                    
                    if removed is None:
                        all_errors.append("remove_ticket() returned None when removing only ticket")
                    elif not isinstance(removed, dict):
                        all_errors.append(f"remove_ticket() should return a dict, got {type(removed)}")
                    elif len(result) != 0:
                        all_errors.append(f"Ticket list should be empty after removing only ticket, got {len(result)}")
                    elif removed != new_ticket:
                        all_errors.append("Removed ticket should match what was added")
            except Exception as e:
                all_errors.append(f"Error testing add/remove with empty list: {str(e)}")
                
            # Test sorting empty ticket list
            try:
                sorted_empty = safely_call_function(self.module_obj, 'sort_tickets', [], "id")
                
                if sorted_empty is None:
                    all_errors.append("sort_tickets() returned None for empty list")
                elif not isinstance(sorted_empty, list):
                    all_errors.append(f"sort_tickets() should return a list, got {type(sorted_empty)}")
                elif sorted_empty != []:
                    all_errors.append(f"Sorting empty list should return empty list, got {sorted_empty}")
            except Exception as e:
                all_errors.append(f"Error sorting empty list: {str(e)}")
                
            # Test filtering empty ticket list
            try:
                filtered_empty = safely_call_function(self.module_obj, 'filter_tickets', [], "type", "technical")
                
                if filtered_empty is None:
                    all_errors.append("filter_tickets() returned None for empty list")
                elif not isinstance(filtered_empty, list):
                    all_errors.append(f"filter_tickets() should return a list, got {type(filtered_empty)}")
                elif filtered_empty != []:
                    all_errors.append(f"Filtering empty list should return empty list, got {filtered_empty}")
            except Exception as e:
                all_errors.append(f"Error filtering empty list: {str(e)}")
                
            # Test minimum/maximum priority values
            try:
                tickets_data = safely_call_function(self.module_obj, 'initialize_data')
                if tickets_data and isinstance(tickets_data, tuple) and len(tickets_data) > 0:
                    tickets = tickets_data[0]
                    
                    if tickets and isinstance(tickets, list):
                        # Get priority 1 tickets (highest priority)
                        min_priority_tickets = safely_call_function(self.module_obj, 'get_priority_tickets', tickets, 1)
                        
                        if min_priority_tickets is None:
                            all_errors.append("get_priority_tickets() returned None for priority 1")
                        elif not isinstance(min_priority_tickets, list):
                            all_errors.append(f"get_priority_tickets() should return a list, got {type(min_priority_tickets)}")
                        elif min_priority_tickets and not all(ticket["priority"] == 1 for ticket in min_priority_tickets):
                            all_errors.append("Minimum priority should be 1 for all returned tickets")
                            
                        # Get priority 4 tickets (lowest priority)
                        max_priority_tickets = safely_call_function(self.module_obj, 'get_priority_tickets', tickets, 4)
                        
                        if max_priority_tickets is None:
                            all_errors.append("get_priority_tickets() returned None for priority 4")
                        elif not isinstance(max_priority_tickets, list):
                            all_errors.append(f"get_priority_tickets() should return a list, got {type(max_priority_tickets)}")
                        elif max_priority_tickets and not all(ticket["priority"] == 4 for ticket in max_priority_tickets):
                            all_errors.append("Maximum priority should be 4 for all returned tickets")
            except Exception as e:
                all_errors.append(f"Error testing min/max priority values: {str(e)}")
                
            # Test combining empty lists
            try:
                tickets_data = safely_call_function(self.module_obj, 'initialize_data')
                if tickets_data and isinstance(tickets_data, tuple) and len(tickets_data) > 1:
                    tickets = tickets_data[0]
                    escalated = tickets_data[1]
                    
                    # Test combining empty list with escalated
                    combined = safely_call_function(self.module_obj, 'combine_queues', [], escalated)
                    
                    if combined is None:
                        all_errors.append("combine_queues() returned None when combining empty list with escalated")
                    elif not isinstance(combined, list):
                        all_errors.append(f"combine_queues() should return a list, got {type(combined)}")
                    elif combined != escalated:
                        all_errors.append(f"Combining empty list with escalated should equal escalated, got different result")
                        
                    # Test combining single tickets
                    if tickets and escalated:
                        combined = safely_call_function(self.module_obj, 'combine_queues', tickets[:1], escalated[:1])
                        
                        if combined is None:
                            all_errors.append("combine_queues() returned None when combining single-ticket lists")
                        elif not isinstance(combined, list):
                            all_errors.append(f"combine_queues() should return a list, got {type(combined)}")
                        elif len(combined) != 2:
                            all_errors.append(f"Combining 1-ticket lists should result in 2 tickets, got {len(combined)}")
            except Exception as e:
                all_errors.append(f"Error testing combining empty lists: {str(e)}")
                
            # Test update on boundary indices
            try:
                tickets_data = safely_call_function(self.module_obj, 'initialize_data')
                if tickets_data and isinstance(tickets_data, tuple) and len(tickets_data) > 0:
                    tickets = tickets_data[0]
                    
                    if tickets and isinstance(tickets, list) and len(tickets) > 0:
                        first_index = 0
                        last_index = len(tickets) - 1
                        
                        # Make a copy to avoid modifying original data
                        test_tickets = tickets.copy()
                        
                        # Update first ticket
                        first_update = safely_call_function(self.module_obj, 'update_ticket', test_tickets, first_index, "status", "resolved")
                        
                        if first_update is None:
                            all_errors.append("update_ticket() returned None when updating first ticket")
                        elif not isinstance(first_update, dict):
                            all_errors.append(f"update_ticket() should return a dict, got {type(first_update)}")
                        elif first_update["status"] != "resolved":
                            all_errors.append(f"Should update first ticket status to 'resolved', got '{first_update['status']}'")
                            
                        # Update last ticket
                        if len(test_tickets) > 1:
                            last_update = safely_call_function(self.module_obj, 'update_ticket', test_tickets, last_index, "status", "closed")
                            
                            if last_update is None:
                                all_errors.append("update_ticket() returned None when updating last ticket")
                            elif not isinstance(last_update, dict):
                                all_errors.append(f"update_ticket() should return a dict, got {type(last_update)}")
                            elif last_update["status"] != "closed":
                                all_errors.append(f"Should update last ticket status to 'closed', got '{last_update['status']}'")
            except Exception as e:
                all_errors.append(f"Error testing update on boundary indices: {str(e)}")
                
            if all_errors:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
            else:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
                print("TestBoundaryScenarios = Passed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            print("TestBoundaryScenarios = Failed")

if __name__ == '__main__':
    unittest.main()