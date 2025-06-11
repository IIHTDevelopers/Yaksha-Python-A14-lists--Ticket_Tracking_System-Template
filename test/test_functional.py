import unittest
import os
import importlib
import sys
import io
import contextlib
import inspect
import re
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

def check_file_exists():
    """Check if the solution file exists"""
    return os.path.isfile('ticket_tracking_system.py')

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_variable_naming(self):
        """Test that the required variable names are used in the solution"""
        try:
            if not check_file_exists():
                self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                print("TestVariableNaming = Failed")
                return
                
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                print("TestVariableNaming = Failed")
                return
                
            all_errors = []
            
            # Check all required functions exist
            required_functions = [
                'initialize_data',
                'add_ticket',
                'remove_ticket',
                'sort_tickets',
                'filter_tickets',
                'combine_queues',
                'get_priority_tickets',
                'manage_queue',
                'update_ticket',
                'get_formatted_ticket',
                'display_data',
                'main'
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
                    
            if missing_functions:
                self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                print("TestVariableNaming = Failed")
                return
                
            # Check initialize_data function returns properly named variables
            try:
                init_source = inspect.getsource(self.module_obj.initialize_data)
                
                # Check for tickets and escalated variables
                if "tickets" not in init_source:
                    all_errors.append("initialize_data() must use variable named 'tickets'")
                    
                if "escalated" not in init_source:
                    all_errors.append("initialize_data() must use variable named 'escalated'")
                    
                # Check for return statement with expected variables
                if "return tickets, escalated," not in init_source:
                    all_errors.append("initialize_data() must return variables named 'tickets', 'escalated', and an empty list")
                    
            except Exception as e:
                all_errors.append(f"Error checking initialize_data() function: {str(e)}")
                
            # Check that the main function uses the required variable names
            try:
                main_source = inspect.getsource(self.module_obj.main)
                
                # Check for proper variable assignment from initialize_data
                if not re.search(r"tickets,\s*escalated,\s*active_queue\s*=\s*initialize_data\(\)", main_source):
                    all_errors.append("main() must assign initialize_data() return values to variables named 'tickets', 'escalated', and 'active_queue'")
            except Exception as e:
                all_errors.append(f"Error checking main() function: {str(e)}")
                
            # Check function parameter names
            try:
                # For add_ticket
                add_source = inspect.getsource(self.module_obj.add_ticket)
                if "def add_ticket(tickets, ticket)" not in add_source:
                    all_errors.append("add_ticket() must use parameter names 'tickets' and 'ticket'")
                    
                # For remove_ticket
                remove_source = inspect.getsource(self.module_obj.remove_ticket)
                if "def remove_ticket(tickets, index)" not in remove_source:
                    all_errors.append("remove_ticket() must use parameter names 'tickets' and 'index'")
                    
                # For sort_tickets
                sort_source = inspect.getsource(self.module_obj.sort_tickets)
                if "def sort_tickets(tickets, key)" not in sort_source:
                    all_errors.append("sort_tickets() must use parameter names 'tickets' and 'key'")
                    
                # For filter_tickets
                filter_source = inspect.getsource(self.module_obj.filter_tickets)
                if "def filter_tickets(tickets, filter_type, value)" not in filter_source:
                    all_errors.append("filter_tickets() must use parameter names 'tickets', 'filter_type', and 'value'")
                    
                # For combine_queues
                combine_source = inspect.getsource(self.module_obj.combine_queues)
                if "def combine_queues(tickets1, tickets2)" not in combine_source:
                    all_errors.append("combine_queues() must use parameter names 'tickets1' and 'tickets2'")
                    
                # For manage_queue
                queue_source = inspect.getsource(self.module_obj.manage_queue)
                if not re.search(r"def\s+manage_queue\s*\(\s*tickets\s*,\s*active_queue\s*,\s*operation\s*,\s*index\s*=", queue_source):
                    all_errors.append("manage_queue() must use parameter names 'tickets', 'active_queue', 'operation', and optional 'index'")
                    
                # For update_ticket
                update_source = inspect.getsource(self.module_obj.update_ticket)
                if "def update_ticket(tickets, index, field, value)" not in update_source:
                    all_errors.append("update_ticket() must use parameter names 'tickets', 'index', 'field', and 'value'")
                    
            except Exception as e:
                all_errors.append(f"Error checking function parameters: {str(e)}")
                
            # Check queue operations in manage_queue
            try:
                queue_source = inspect.getsource(self.module_obj.manage_queue)
                
                if "active_queue.append" not in queue_source:
                    all_errors.append("manage_queue must use append() method on active_queue for adding items")
                    
                if "active_queue.pop" not in queue_source and "active_queue.remove" not in queue_source:
                    all_errors.append("manage_queue must use pop() or remove() method on active_queue for removing items")
                    
                if "active_queue.clear" not in queue_source:
                    all_errors.append("manage_queue must use clear() method on active_queue for clearing items")
                    
            except Exception as e:
                all_errors.append(f"Error checking queue operations in manage_queue(): {str(e)}")
                
            # Check initialize_data for predefined tickets
            try:
                init_source = inspect.getsource(self.module_obj.initialize_data)
                
                # Check for predefined ticket IDs
                ticket_ids = ['"T001"', '"T002"', '"T003"', '"T004"', '"T005"']
                for ticket_id in ticket_ids:
                    if ticket_id not in init_source:
                        all_errors.append(f"initialize_data() must contain ticket with ID {ticket_id}")
                        
                # Check for escalated ticket IDs
                escalated_ids = ['"E001"', '"E002"']
                for ticket_id in escalated_ids:
                    if ticket_id not in init_source:
                        all_errors.append(f"initialize_data() must contain escalated ticket with ID {ticket_id}")
                        
            except Exception as e:
                all_errors.append(f"Error checking predefined tickets in initialize_data(): {str(e)}")
                
            if all_errors:
                self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                print("TestVariableNaming = Failed")
            else:
                self.test_obj.yakshaAssert("TestVariableNaming", True, "functional")
                print("TestVariableNaming = Passed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
            print("TestVariableNaming = Failed")

    def test_ticket_operations(self):
        """Test basic ticket operations"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestTicketOperations", False, "functional")
                print("TestTicketOperations = Failed")
                return
                
            # Check if required functions exist
            required_functions = ['add_ticket', 'remove_ticket', 'sort_tickets', 'filter_tickets']
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
                    
            if missing_functions:
                self.test_obj.yakshaAssert("TestTicketOperations", False, "functional")
                print("TestTicketOperations = Failed")
                return
                
            sample_tickets = safely_call_function(self.module_obj, 'initialize_data')
            if not sample_tickets or not isinstance(sample_tickets, tuple) or len(sample_tickets) < 1:
                self.test_obj.yakshaAssert("TestTicketOperations", False, "functional")
                print("TestTicketOperations = Failed")
                return
                
            sample_tickets = sample_tickets[0]
            if not sample_tickets:
                self.test_obj.yakshaAssert("TestTicketOperations", False, "functional")
                print("TestTicketOperations = Failed")
                return
                
            all_errors = []
            original_len = len(sample_tickets)
            
            # Test add_ticket
            try:
                new_ticket = {"id": "T006", "title": "Test Ticket", "type": "technical", "priority": 2, "status": "new"}
                updated_tickets = safely_call_function(self.module_obj, 'add_ticket', sample_tickets.copy(), new_ticket)
                
                if updated_tickets is None:
                    all_errors.append("add_ticket() returned None instead of the updated list")
                elif not isinstance(updated_tickets, list):
                    all_errors.append(f"add_ticket() should return a list, got {type(updated_tickets)}")
                elif len(updated_tickets) != original_len + 1:
                    all_errors.append(f"Adding ticket should increase list size by 1, got {len(updated_tickets)}")
                elif updated_tickets[-1] != new_ticket:
                    all_errors.append("Added ticket should be at the end of list")
            except Exception as e:
                all_errors.append(f"Error testing add_ticket(): {str(e)}")
                
            # Test remove_ticket
            try:
                test_tickets = sample_tickets.copy()
                # Add a ticket first to ensure we have something to remove
                test_ticket = {"id": "T006", "title": "Test Ticket", "type": "technical", "priority": 2, "status": "new"}
                test_tickets.append(test_ticket)
                
                removed = safely_call_function(self.module_obj, 'remove_ticket', test_tickets, len(test_tickets) - 1)
                
                if removed is None:
                    all_errors.append("remove_ticket() returned None instead of the removed ticket")
                elif not isinstance(removed, dict):
                    all_errors.append(f"remove_ticket() should return a dictionary, got {type(removed)}")
                elif len(test_tickets) != original_len:
                    all_errors.append(f"Removing ticket should decrease list size back to original, got {len(test_tickets)}")
                elif removed != test_ticket:
                    all_errors.append("Removed ticket should match the added ticket")
            except Exception as e:
                all_errors.append(f"Error testing remove_ticket(): {str(e)}")
                
            # Test sort_tickets by different keys
            try:
                # Sort by priority
                sorted_by_priority = safely_call_function(self.module_obj, 'sort_tickets', sample_tickets.copy(), "priority")
                
                if sorted_by_priority is None:
                    all_errors.append("sort_tickets() returned None instead of sorted list")
                elif not isinstance(sorted_by_priority, list):
                    all_errors.append(f"sort_tickets() should return a list, got {type(sorted_by_priority)}")
                elif len(sorted_by_priority) != len(sample_tickets):
                    all_errors.append("Sorted list should have same length as original list")
                elif len(sorted_by_priority) > 1 and sorted_by_priority[0]["priority"] > sorted_by_priority[-1]["priority"]:
                    all_errors.append("Tickets should be sorted by priority (low to high)")
                    
                # Sort by id
                sorted_by_id = safely_call_function(self.module_obj, 'sort_tickets', sample_tickets.copy(), "id")
                
                if sorted_by_id is None:
                    all_errors.append("sort_tickets() returned None instead of sorted list")
                elif not isinstance(sorted_by_id, list):
                    all_errors.append(f"sort_tickets() should return a list, got {type(sorted_by_id)}")
                elif len(sorted_by_id) != len(sample_tickets):
                    all_errors.append("Sorted list should have same length as original list")
                elif len(sorted_by_id) > 1:
                    id_order = [ticket["id"] for ticket in sorted_by_id]
                    sorted_ids = sorted(id_order)
                    if id_order != sorted_ids:
                        all_errors.append("Tickets should be sorted by id ascending")
            except Exception as e:
                all_errors.append(f"Error testing sort_tickets(): {str(e)}")
                
            # Test filter_tickets
            try:
                # Find a ticket type that exists in the sample data
                if len(sample_tickets) > 0:
                    existing_type = sample_tickets[0]["type"]
                    
                    # Filter by type
                    type_filtered = safely_call_function(self.module_obj, 'filter_tickets', sample_tickets, "type", existing_type)
                    
                    if type_filtered is None:
                        all_errors.append("filter_tickets() by type returned None instead of filtered list")
                    elif not isinstance(type_filtered, list):
                        all_errors.append(f"filter_tickets() should return a list, got {type(type_filtered)}")
                    elif not all(ticket["type"] == existing_type for ticket in type_filtered):
                        all_errors.append(f"All filtered tickets should have type '{existing_type}'")
                        
                    # Find a status that exists in the sample data
                    existing_status = sample_tickets[0]["status"]
                    
                    # Filter by status
                    status_filtered = safely_call_function(self.module_obj, 'filter_tickets', sample_tickets, "status", existing_status)
                    
                    if status_filtered is None:
                        all_errors.append("filter_tickets() by status returned None instead of filtered list")
                    elif not isinstance(status_filtered, list):
                        all_errors.append(f"filter_tickets() should return a list, got {type(status_filtered)}")
                    elif not all(ticket["status"] == existing_status for ticket in status_filtered):
                        all_errors.append(f"All filtered tickets should have status '{existing_status}'")
                        
                    # Find a word that exists in at least one ticket title
                    if "payment" in sample_tickets[0]["title"].lower():
                        keyword = "payment"
                    elif len(sample_tickets) > 1 and "password" in sample_tickets[1]["title"].lower():
                        keyword = "password"
                    else:
                        keyword = sample_tickets[0]["title"].split()[0].lower()
                    
                    # Filter by keyword
                    keyword_filtered = safely_call_function(self.module_obj, 'filter_tickets', sample_tickets, "keyword", keyword)
                    
                    if keyword_filtered is None:
                        all_errors.append("filter_tickets() by keyword returned None instead of filtered list")
                    elif not isinstance(keyword_filtered, list):
                        all_errors.append(f"filter_tickets() should return a list, got {type(keyword_filtered)}")
                    elif len(keyword_filtered) > 0 and not all(keyword in ticket["title"].lower() for ticket in keyword_filtered):
                        all_errors.append(f"All filtered tickets should contain keyword '{keyword}'")
            except Exception as e:
                all_errors.append(f"Error testing filter_tickets(): {str(e)}")
                
            if all_errors:
                self.test_obj.yakshaAssert("TestTicketOperations", False, "functional")
                print("TestTicketOperations = Failed")
            else:
                self.test_obj.yakshaAssert("TestTicketOperations", True, "functional")
                print("TestTicketOperations = Passed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestTicketOperations", False, "functional")
            print("TestTicketOperations = Failed")

    def test_list_specific_operations(self):
        """Test list-specific operations like combining"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestListSpecificOperations", False, "functional")
                print("TestListSpecificOperations = Failed")
                return
                
            # Check if required functions exist
            required_functions = ['combine_queues', 'get_priority_tickets']
            missing_functions = []
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    missing_functions.append(func_name)
                    
            if missing_functions:
                self.test_obj.yakshaAssert("TestListSpecificOperations", False, "functional")
                print("TestListSpecificOperations = Failed")
                return
                
            tickets_data = safely_call_function(self.module_obj, 'initialize_data')
            if not tickets_data or not isinstance(tickets_data, tuple) or len(tickets_data) < 2:
                self.test_obj.yakshaAssert("TestListSpecificOperations", False, "functional")
                print("TestListSpecificOperations = Failed")
                return
                
            sample_tickets = tickets_data[0]
            sample_escalated = tickets_data[1]
            
            if not sample_tickets or not sample_escalated:
                self.test_obj.yakshaAssert("TestListSpecificOperations", False, "functional")
                print("TestListSpecificOperations = Failed")
                return
                
            all_errors = []
            
            # Test combine_queues
            try:
                combined = safely_call_function(self.module_obj, 'combine_queues', sample_tickets, sample_escalated)
                
                if combined is None:
                    all_errors.append("combine_queues() returned None instead of combined list")
                elif not isinstance(combined, list):
                    all_errors.append(f"combine_queues() should return a list, got {type(combined)}")
                elif len(combined) != len(sample_tickets) + len(sample_escalated):
                    all_errors.append(f"Combined list should contain all tickets. Expected {len(sample_tickets) + len(sample_escalated)}, got {len(combined)}")
                    
                # Verify the combined list contains tickets from both original lists
                for ticket in sample_tickets:
                    if ticket not in combined:
                        all_errors.append(f"Combined list should contain original ticket {ticket['id']}")
                
                for ticket in sample_escalated:
                    if ticket not in combined:
                        all_errors.append(f"Combined list should contain escalated ticket {ticket['id']}")
            except Exception as e:
                all_errors.append(f"Error testing combine_queues(): {str(e)}")
                
            # Test priority filtering
            try:
                # Find a priority that exists in the sample data
                if len(sample_tickets) > 0:
                    existing_priority = sample_tickets[0]["priority"]
                    
                    priority_tickets = safely_call_function(self.module_obj, 'get_priority_tickets', sample_tickets, existing_priority)
                    
                    if priority_tickets is None:
                        all_errors.append("get_priority_tickets() returned None instead of filtered list")
                    elif not isinstance(priority_tickets, list):
                        all_errors.append(f"get_priority_tickets() should return a list, got {type(priority_tickets)}")
                    elif not all(ticket["priority"] == existing_priority for ticket in priority_tickets):
                        all_errors.append(f"All tickets should have priority {existing_priority}")
            except Exception as e:
                all_errors.append(f"Error testing get_priority_tickets(): {str(e)}")
                
            if all_errors:
                self.test_obj.yakshaAssert("TestListSpecificOperations", False, "functional")
                print("TestListSpecificOperations = Failed")
            else:
                self.test_obj.yakshaAssert("TestListSpecificOperations", True, "functional")
                print("TestListSpecificOperations = Passed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestListSpecificOperations", False, "functional")
            print("TestListSpecificOperations = Failed")

    def test_queue_management(self):
        """Test active queue functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestQueueManagement", False, "functional")
                print("TestQueueManagement = Failed")
                return
                
            # Check if required functions exist
            if not check_function_exists(self.module_obj, 'manage_queue'):
                self.test_obj.yakshaAssert("TestQueueManagement", False, "functional")
                print("TestQueueManagement = Failed")
                return
                
            tickets_data = safely_call_function(self.module_obj, 'initialize_data')
            if not tickets_data or not isinstance(tickets_data, tuple) or len(tickets_data) < 1:
                self.test_obj.yakshaAssert("TestQueueManagement", False, "functional")
                print("TestQueueManagement = Failed")
                return
                
            sample_tickets = tickets_data[0]
            if not sample_tickets:
                self.test_obj.yakshaAssert("TestQueueManagement", False, "functional")
                print("TestQueueManagement = Failed")
                return
                
            all_errors = []
            active_queue = []
            
            # Test add to queue
            try:
                for i in range(min(3, len(sample_tickets))):
                    updated_queue = safely_call_function(self.module_obj, 'manage_queue', sample_tickets, active_queue, "add", i)
                    
                    if updated_queue is None:
                        all_errors.append(f"manage_queue(add) returned None instead of updated queue")
                        break
                    elif not isinstance(updated_queue, list):
                        all_errors.append(f"manage_queue() should return a list, got {type(updated_queue)}")
                        break
                    elif len(updated_queue) != i + 1:
                        all_errors.append(f"Queue should have {i+1} tickets after adding, got {len(updated_queue)}")
                        break
                    elif updated_queue[i] != sample_tickets[i]:
                        all_errors.append(f"Added ticket should match original ticket at index {i}")
                        break
            except Exception as e:
                all_errors.append(f"Error testing manage_queue(add): {str(e)}")
                
            # Skip removal and clear tests if add failed
            if not all_errors:
                # Test remove from queue
                try:
                    if len(active_queue) >= 2:
                        removed = safely_call_function(self.module_obj, 'manage_queue', sample_tickets, active_queue, "remove", 1)
                        
                        if removed is None:
                            all_errors.append(f"manage_queue(remove) returned None instead of removed ticket")
                        elif not isinstance(removed, dict):
                            all_errors.append(f"manage_queue(remove) should return a dict, got {type(removed)}")
                        elif len(active_queue) != 2:
                            all_errors.append(f"Queue should have 2 tickets after removing one, got {len(active_queue)}")
                        elif removed != sample_tickets[1]:
                            all_errors.append(f"Removed ticket should match the original")
                except Exception as e:
                    all_errors.append(f"Error testing manage_queue(remove): {str(e)}")
                    
                # Test clear queue
                try:
                    cleared = safely_call_function(self.module_obj, 'manage_queue', sample_tickets, active_queue, "clear")
                    
                    if cleared is None:
                        all_errors.append(f"manage_queue(clear) returned None instead of cleared queue")
                    elif not isinstance(cleared, list):
                        all_errors.append(f"manage_queue(clear) should return a list, got {type(cleared)}")
                    elif len(cleared) != 0:
                        all_errors.append(f"Cleared queue should be empty, got {len(cleared)}")
                except Exception as e:
                    all_errors.append(f"Error testing manage_queue(clear): {str(e)}")
                    
            if all_errors:
                self.test_obj.yakshaAssert("TestQueueManagement", False, "functional")
                print("TestQueueManagement = Failed")
            else:
                self.test_obj.yakshaAssert("TestQueueManagement", True, "functional")
                print("TestQueueManagement = Passed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestQueueManagement", False, "functional")
            print("TestQueueManagement = Failed")

    def test_ticket_updates(self):
        """Test ticket update functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestTicketUpdates", False, "functional")
                print("TestTicketUpdates = Failed")
                return
                
            # Check if required functions exist
            if not check_function_exists(self.module_obj, 'update_ticket'):
                self.test_obj.yakshaAssert("TestTicketUpdates", False, "functional")
                print("TestTicketUpdates = Failed")
                return
                
            tickets_data = safely_call_function(self.module_obj, 'initialize_data')
            if not tickets_data or not isinstance(tickets_data, tuple) or len(tickets_data) < 1:
                self.test_obj.yakshaAssert("TestTicketUpdates", False, "functional")
                print("TestTicketUpdates = Failed")
                return
                
            sample_tickets = tickets_data[0]
            if not sample_tickets:
                self.test_obj.yakshaAssert("TestTicketUpdates", False, "functional")
                print("TestTicketUpdates = Failed")
                return
                
            all_errors = []
            
            # Test update ticket status
            try:
                test_tickets = sample_tickets.copy()
                index = 0
                original_status = test_tickets[index]["status"]
                new_status = "resolved" if original_status != "resolved" else "closed"
                
                updated = safely_call_function(self.module_obj, 'update_ticket', test_tickets, index, "status", new_status)
                
                if updated is None:
                    all_errors.append("update_ticket() returned None instead of updated ticket")
                elif not isinstance(updated, dict):
                    all_errors.append(f"update_ticket() should return a dict, got {type(updated)}")
                elif updated["status"] != new_status:
                    all_errors.append(f"Status should be updated to {new_status}, got {updated['status']}")
                    
                # Verify the original list was also updated
                if test_tickets[index]["status"] != new_status:
                    all_errors.append(f"Original list should also be updated with new status")
            except Exception as e:
                all_errors.append(f"Error testing update_ticket(status): {str(e)}")
                
            # Test update ticket priority
            try:
                test_tickets = sample_tickets.copy()
                
                if len(test_tickets) > 1:
                    index = 1
                    original_priority = test_tickets[index]["priority"]
                    new_priority = 2 if original_priority != 2 else 3
                    
                    updated = safely_call_function(self.module_obj, 'update_ticket', test_tickets, index, "priority", str(new_priority))
                    
                    if updated is None:
                        all_errors.append("update_ticket() returned None instead of updated ticket")
                    elif not isinstance(updated, dict):
                        all_errors.append(f"update_ticket() should return a dict, got {type(updated)}")
                    elif updated["priority"] != new_priority:
                        all_errors.append(f"Priority should be updated to {new_priority}, got {updated['priority']}")
                        
                    # Verify the original list was also updated
                    if test_tickets[index]["priority"] != new_priority:
                        all_errors.append(f"Original list should also be updated with new priority")
            except Exception as e:
                all_errors.append(f"Error testing update_ticket(priority): {str(e)}")
                
            if all_errors:
                self.test_obj.yakshaAssert("TestTicketUpdates", False, "functional")
                print("TestTicketUpdates = Failed")
            else:
                self.test_obj.yakshaAssert("TestTicketUpdates", True, "functional")
                print("TestTicketUpdates = Passed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestTicketUpdates", False, "functional")
            print("TestTicketUpdates = Failed")

    def test_display_functions(self):
        """Test display functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestDisplayFunctions", False, "functional")
                print("TestDisplayFunctions = Failed")
                return
                
            # Check if required functions exist
            if not check_function_exists(self.module_obj, 'get_formatted_ticket'):
                self.test_obj.yakshaAssert("TestDisplayFunctions", False, "functional")
                print("TestDisplayFunctions = Failed")
                return
                
            tickets_data = safely_call_function(self.module_obj, 'initialize_data')
            if not tickets_data or not isinstance(tickets_data, tuple) or len(tickets_data) < 1:
                self.test_obj.yakshaAssert("TestDisplayFunctions", False, "functional")
                print("TestDisplayFunctions = Failed")
                return
                
            sample_tickets = tickets_data[0]
            if not sample_tickets:
                self.test_obj.yakshaAssert("TestDisplayFunctions", False, "functional")
                print("TestDisplayFunctions = Failed")
                return
                
            all_errors = []
            
            # Test get_formatted_ticket
            try:
                ticket = sample_tickets[0]
                ticket_display = safely_call_function(self.module_obj, 'get_formatted_ticket', ticket)
                
                if ticket_display is None:
                    all_errors.append("get_formatted_ticket() returned None instead of formatted string")
                elif not isinstance(ticket_display, str):
                    all_errors.append(f"get_formatted_ticket() should return a string, got {type(ticket_display)}")
                else:
                    # Check format contains required elements
                    required_elements = [
                        ticket["id"],
                        ticket["title"],
                        ticket["type"],
                        "Priority",
                        str(ticket["priority"]),
                        "Status",
                        ticket["status"].upper()
                    ]
                    
                    for element in required_elements:
                        if element not in ticket_display:
                            all_errors.append(f"Ticket display should contain '{element}'")
                    
                    # Check for priority indicator words
                    priority_indicators = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
                    if not any(indicator in ticket_display for indicator in priority_indicators):
                        all_errors.append("Display should show priority indicator (CRITICAL, HIGH, MEDIUM, or LOW)")
            except Exception as e:
                all_errors.append(f"Error testing get_formatted_ticket(): {str(e)}")
                
            if all_errors:
                self.test_obj.yakshaAssert("TestDisplayFunctions", False, "functional")
                print("TestDisplayFunctions = Failed")
            else:
                self.test_obj.yakshaAssert("TestDisplayFunctions", True, "functional")
                print("TestDisplayFunctions = Passed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestDisplayFunctions", False, "functional")
            print("TestDisplayFunctions = Failed")

if __name__ == '__main__':
    unittest.main()