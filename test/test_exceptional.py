import pytest
from test.TestUtils import TestUtils
from ticket_tracking_system import *  # Import all functions directly

@pytest.fixture
def test_obj():
    return TestUtils()

def test_invalid_input_handling(test_obj):
    """Consolidated test for invalid input validation"""
    try:
        tickets, _, _ = initialize_data()
        active_queue = []
        
        # Test adding invalid ticket
        invalid_ticket = {"id": "X999", "title": "Invalid"}  # Missing required fields
        with pytest.raises(ValueError):
            add_ticket(tickets, invalid_ticket)
        
        # Test invalid ticket type
        invalid_ticket = {"id": "T999", "title": "Invalid", "type": "invalid_type", "priority": 2, "status": "new"}
        with pytest.raises(ValueError):
            add_ticket(tickets, invalid_ticket)
        
        # Test invalid priority
        invalid_ticket = {"id": "T999", "title": "Invalid", "type": "technical", "priority": 10, "status": "new"}
        with pytest.raises(ValueError):
            add_ticket(tickets, invalid_ticket)
        
        # Test invalid status
        invalid_ticket = {"id": "T999", "title": "Invalid", "type": "technical", "priority": 2, "status": "invalid_status"}
        with pytest.raises(ValueError):
            add_ticket(tickets, invalid_ticket)
        
        # Test out of range index for removing ticket
        with pytest.raises(IndexError):
            remove_ticket(tickets, len(tickets) + 5)
        
        # Test invalid sort key
        with pytest.raises(ValueError):
            sort_tickets(tickets, "invalid_key")
        
        # Test invalid filter type
        with pytest.raises(ValueError):
            filter_tickets(tickets, "invalid_filter", "value")
        
        # Test invalid priority level
        with pytest.raises(ValueError):
            get_priority_tickets(tickets, 0)
        
        with pytest.raises(ValueError):
            get_priority_tickets(tickets, 5)
        
        # Test queue management with invalid operation
        with pytest.raises(ValueError):
            manage_queue(tickets, active_queue, "invalid_operation")
        
        # Test queue with invalid index
        with pytest.raises(IndexError):
            manage_queue(tickets, active_queue, "add", len(tickets) + 10)
        
        # Test queue size limit
        # First, fill the queue to max capacity
        for i in range(5):
            manage_queue(tickets, active_queue, "add", i)
        
        # Then try to add one more ticket
        with pytest.raises(ValueError):
            manage_queue(tickets, active_queue, "add", 0)
        
        # Clear queue for next tests
        manage_queue(tickets, active_queue, "clear")
        
        # Test remove from queue with invalid index
        with pytest.raises(IndexError):
            manage_queue(tickets, active_queue, "remove", 0)  # Empty queue
        
        # Test update with invalid index
        with pytest.raises(IndexError):
            update_ticket(tickets, len(tickets) + 5, "status", "resolved")
        
        # Test update with invalid status
        with pytest.raises(ValueError):
            update_ticket(tickets, 0, "status", "invalid_status")
        
        # Test update with invalid priority
        with pytest.raises(ValueError):
            update_ticket(tickets, 0, "priority", "10")
        
        test_obj.yakshaAssert("TestInvalidInputHandling", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestInvalidInputHandling", False, "exception")
        pytest.fail(f"Invalid input handling test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])