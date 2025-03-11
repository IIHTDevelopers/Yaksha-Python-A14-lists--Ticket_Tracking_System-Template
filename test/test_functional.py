import pytest
import inspect
import importlib
import re
from test.TestUtils import TestUtils
from ticket_tracking_system import *  # Import all functions directly

@pytest.fixture
def test_obj():
    return TestUtils()

@pytest.fixture
def sample_tickets():
    """Sample tickets for testing"""
    return initialize_data()[0]  # First element is tickets

@pytest.fixture
def sample_escalated():
    """Sample escalated tickets for testing"""
    return initialize_data()[1]  # Second element is escalated

def test_variable_naming(test_obj):
    """Test that the required variable names are used in the solution"""
    try:
        # Import the module
        try:
            module = importlib.import_module("solution")
        except ImportError:
            # Try alternative module name
            try:
                module = importlib.import_module("ticket_tracking_system")
            except ImportError:
                raise ImportError("Could not import solution module. Make sure it's named 'solution.py' or 'ticket_tracking_system.py'")

        # Check initialize_data function returns properly named variables
        init_source = inspect.getsource(module.initialize_data)
        
        # Check for return statement with the expected variable names
        assert "return tickets, escalated," in init_source, "initialize_data() must return variables named 'tickets', 'escalated', and an empty list"
        
        # Check that the main function uses the required variable names
        main_source = inspect.getsource(module.main)
        
        # Check for proper variable assignment from initialize_data
        assert re.search(r"tickets,\s*escalated,\s*active_queue\s*=\s*initialize_data\(\)", main_source), "main() must assign initialize_data() return values to variables named 'tickets', 'escalated', and 'active_queue'"
        
        # Check if the variable names are used in the appropriate functions
        # For add_ticket and remove_ticket
        assert "def add_ticket(tickets, ticket)" in inspect.getsource(module), "add_ticket() must use the parameter name 'tickets'"
        assert "def remove_ticket(tickets, index)" in inspect.getsource(module), "remove_ticket() must use the parameter name 'tickets'"
        
        # For sort_tickets and filter_tickets
        assert "def sort_tickets(tickets, key)" in inspect.getsource(module), "sort_tickets() must use the parameter name 'tickets'"
        assert "def filter_tickets(tickets, filter_type, value)" in inspect.getsource(module), "filter_tickets() must use the parameter names 'tickets', 'filter_type', and 'value'"
        
        # For combine_queues
        combine_source = inspect.getsource(module.combine_queues)
        assert "def combine_queues(tickets1, tickets2)" in combine_source, "combine_queues() must use parameter names 'tickets1' and 'tickets2'"
        
        # For manage_queue
        queue_source = inspect.getsource(module.manage_queue)
        assert "def manage_queue(tickets, active_queue, operation, index=" in queue_source, "manage_queue() must use parameter names 'tickets', 'active_queue', 'operation', and optional 'index'"
        
        # For update_ticket
        update_source = inspect.getsource(module.update_ticket)
        assert "def update_ticket(tickets, index, field, value)" in update_source, "update_ticket() must use parameter names 'tickets', 'index', 'field', and 'value'"
        
        # Check that the active_queue variable is used correctly
        assert "active_queue.append" in queue_source, "manage_queue must use append() method on active_queue for adding items"
        assert "active_queue.pop" in queue_source, "manage_queue must use pop() method on active_queue for removing items"
        assert "active_queue.clear" in queue_source, "manage_queue must use clear() method on active_queue for clearing items"
        
        # Check predefined tickets exist with right IDs
        assert '"T001"' in init_source, "initialize_data() must contain ticket with ID 'T001'"
        assert '"T002"' in init_source, "initialize_data() must contain ticket with ID 'T002'"
        assert '"T003"' in init_source, "initialize_data() must contain ticket with ID 'T003'"
        assert '"T004"' in init_source, "initialize_data() must contain ticket with ID 'T004'"
        assert '"T005"' in init_source, "initialize_data() must contain ticket with ID 'T005'"
        
        # Check escalated tickets
        assert '"E001"' in init_source, "initialize_data() must contain escalated ticket with ID 'E001'"
        assert '"E002"' in init_source, "initialize_data() must contain escalated ticket with ID 'E002'"
        
        test_obj.yakshaAssert("TestVariableNaming", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestVariableNaming", False, "functional")
        pytest.fail(f"Variable naming test failed: {str(e)}")

def test_ticket_operations(test_obj, sample_tickets):
    """Test basic ticket operations"""
    try:
        original_len = len(sample_tickets)
        
        # Test add_ticket
        new_ticket = {"id": "T006", "title": "Test Ticket", "type": "technical", "priority": 2, "status": "new"}
        updated_tickets = add_ticket(sample_tickets, new_ticket)
        assert len(updated_tickets) == original_len + 1, "Adding ticket should increase list size by 1"
        assert updated_tickets[-1] == new_ticket, "Added ticket should be at the end of list"
        
        # Test remove_ticket
        removed = remove_ticket(sample_tickets, len(sample_tickets) - 1)
        assert len(sample_tickets) == original_len, "Removing ticket should decrease list size back to original"
        assert removed == new_ticket, "Removed ticket should match the added ticket"
        
        # Test sort_tickets by different keys
        # Store original order to verify sorting changed something
        original_order = [ticket["id"] for ticket in sample_tickets]
        
        # Sort by priority
        sorted_by_priority = sort_tickets(sample_tickets.copy(), "priority")
        # Check if high priority tickets (low numbers) are first
        assert sorted_by_priority[0]["priority"] <= sorted_by_priority[-1]["priority"], "Tickets should be sorted by priority (high to low)"
        
        # Sort by id
        sorted_by_id = sort_tickets(sample_tickets.copy(), "id")
        id_order = [ticket["id"] for ticket in sorted_by_id]
        assert id_order == sorted(id_order), "Tickets should be sorted by id ascending"
        
        # Test filter_tickets
        # Filter by type
        technical = filter_tickets(sample_tickets, "type", "technical")
        assert all(ticket["type"] == "technical" for ticket in technical), "All filtered tickets should be technical"
        
        # Filter by status
        open_tickets = filter_tickets(sample_tickets, "status", "open")
        assert all(ticket["status"] == "open" for ticket in open_tickets), "All filtered tickets should have open status"
        
        # Filter by keyword
        keyword_tickets = filter_tickets(sample_tickets, "keyword", "payment")
        assert all("payment" in ticket["title"].lower() for ticket in keyword_tickets), "All filtered tickets should contain keyword 'payment'"
        
        test_obj.yakshaAssert("TestTicketOperations", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestTicketOperations", False, "functional")
        pytest.fail(f"Ticket operations test failed: {str(e)}")

def test_list_specific_operations(test_obj, sample_tickets, sample_escalated):
    """Test list-specific operations like combining"""
    try:
        # Test combine_queues
        combined = combine_queues(sample_tickets, sample_escalated)
        assert len(combined) == len(sample_tickets) + len(sample_escalated), "Combined list should contain all tickets"
        
        # Verify the combined list contains tickets from both original lists
        for ticket in sample_tickets:
            assert ticket in combined, "Combined list should contain original tickets"
        
        for ticket in sample_escalated:
            assert ticket in combined, "Combined list should contain escalated tickets"
        
        # Test priority filtering
        priority_tickets = get_priority_tickets(sample_tickets, 1)
        assert all(ticket["priority"] == 1 for ticket in priority_tickets), "All tickets should have priority 1"
        
        test_obj.yakshaAssert("TestListSpecificOperations", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestListSpecificOperations", False, "functional")
        pytest.fail(f"List specific operations test failed: {str(e)}")

def test_queue_management(test_obj, sample_tickets):
    """Test active queue functions"""
    try:
        active_queue = []
        
        # Test add to queue
        for i in range(3):
            updated_queue = manage_queue(sample_tickets, active_queue, "add", i)
            assert len(updated_queue) == i + 1, f"Queue should have {i+1} tickets after adding"
            assert updated_queue[i] == sample_tickets[i], "Added ticket should match original ticket"
        
        # Test remove from queue
        removed = manage_queue(sample_tickets, active_queue, "remove", 1)
        assert len(active_queue) == 2, "Queue should have 2 tickets after removing one"
        assert removed == sample_tickets[1], "Removed ticket should match the original"
        
        # Test clear queue
        cleared = manage_queue(sample_tickets, active_queue, "clear")
        assert len(cleared) == 0, "Cleared queue should be empty"
        
        test_obj.yakshaAssert("TestQueueManagement", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestQueueManagement", False, "functional")
        pytest.fail(f"Queue management test failed: {str(e)}")

def test_ticket_updates(test_obj, sample_tickets):
    """Test ticket update functions"""
    try:
        # Test update ticket status
        index = 0
        original_status = sample_tickets[index]["status"]
        new_status = "resolved" if original_status != "resolved" else "closed"
        
        updated = update_ticket(sample_tickets, index, "status", new_status)
        assert updated["status"] == new_status, f"Status should be updated to {new_status}"
        
        # Test update ticket priority
        index = 1
        original_priority = sample_tickets[index]["priority"]
        new_priority = 2 if original_priority != 2 else 3
        
        updated = update_ticket(sample_tickets, index, "priority", str(new_priority))
        assert updated["priority"] == new_priority, f"Priority should be updated to {new_priority}"
        
        test_obj.yakshaAssert("TestTicketUpdates", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestTicketUpdates", False, "functional")
        pytest.fail(f"Ticket update test failed: {str(e)}")

def test_display_functions(test_obj, sample_tickets):
    """Test display functions"""
    try:
        # Test get_formatted_ticket
        ticket = sample_tickets[0]
        ticket_display = get_formatted_ticket(ticket)
        
        # Check format contains required elements
        assert ticket["id"] in ticket_display, "Ticket display should contain ID"
        assert ticket["title"] in ticket_display, "Ticket display should contain title"
        assert ticket["type"] in ticket_display, "Ticket display should contain type"
        assert "Priority" in ticket_display, "Ticket display should mention priority"
        
        # Test priority indicator
        priority_indicators = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        assert any(indicator in ticket_display for indicator in priority_indicators), "Display should show priority indicator"
        
        # Test status indicator
        status_indicators = ["NEW", "OPEN", "RESOLVED", "CLOSED"]
        assert any(indicator in ticket_display for indicator in status_indicators), "Display should show status indicator"
        
        test_obj.yakshaAssert("TestDisplayFunctions", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestDisplayFunctions", False, "functional")
        pytest.fail(f"Display functions test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])