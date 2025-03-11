import pytest
from test.TestUtils import TestUtils
from ticket_tracking_system import *  # Import all functions directly

@pytest.fixture
def test_obj():
    return TestUtils()

def test_boundary_scenarios(test_obj):
    """Consolidated test for boundary scenarios"""
    try:
        # Test with empty ticket list
        empty_tickets = []
        active_queue = []
        
        # Test queue size limit
        tickets, _, _ = initialize_data()
        
        # Add 5 tickets to queue (maximum allowed)
        for i in range(5):
            manage_queue(tickets, active_queue, "add", i)
        
        assert len(active_queue) == 5, "Queue should allow exactly 5 tickets"
        
        # Test adding tickets to an empty list
        new_ticket = {"id": "T100", "title": "Test ticket", "type": "technical", "priority": 2, "status": "new"}
        result = add_ticket(empty_tickets, new_ticket)
        assert len(result) == 1, "Should be able to add ticket to empty list"
        
        # Test removing the only ticket
        removed = remove_ticket(result, 0)
        assert len(result) == 0, "Ticket list should be empty after removing only ticket"
        assert removed == new_ticket, "Removed ticket should match what was added"
        
        # Test sorting empty ticket list
        sorted_empty = sort_tickets([], "id")
        assert sorted_empty == [], "Sorting empty list should return empty list"
        
        # Test filtering empty ticket list
        filtered_empty = filter_tickets([], "type", "technical")
        assert filtered_empty == [], "Filtering empty list should return empty list"
        
        # Test minimum/maximum priority values
        tickets, _, _ = initialize_data()
        min_priority_tickets = get_priority_tickets(tickets, 1)  # Critical
        max_priority_tickets = get_priority_tickets(tickets, 4)  # Low
        
        if min_priority_tickets:
            assert all(ticket["priority"] == 1 for ticket in min_priority_tickets), "Minimum priority should be 1"
        
        if max_priority_tickets:
            assert all(ticket["priority"] == 4 for ticket in max_priority_tickets), "Maximum priority should be 4"
        
        # Test combining empty lists
        tickets, escalated, _ = initialize_data()
        combined = combine_queues([], escalated)
        assert combined == escalated, "Combining empty list with escalated should equal escalated"
        
        combined = combine_queues(tickets[:1], escalated[:1])
        assert len(combined) == 2, "Combining 1-ticket lists should result in 2 tickets"
        
        # Test update on boundary indices
        if tickets:
            first_index = 0
            last_index = len(tickets) - 1
            
            # Update first ticket
            update_ticket(tickets, first_index, "status", "resolved")
            assert tickets[first_index]["status"] == "resolved", "Should update first ticket"
            
            # Update last ticket
            update_ticket(tickets, last_index, "status", "closed")
            assert tickets[last_index]["status"] == "closed", "Should update last ticket"
        
        test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
        pytest.fail(f"Boundary scenarios test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])