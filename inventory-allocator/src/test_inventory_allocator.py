import unittest
from inventory_allocator import InventoryAllocator

class TestInventoryAllocator(unittest.TestCase):
  def test_single_shipment_single_item(self):
    allocator = InventoryAllocator(
      { 'apple': 1 },
      [{ 'name': 'owd', 'inventory': { 'apple': 1 } }]
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      [{ 'owd': { 'apple': 1 } }]
    )

  def test_single_shipment_multiple_items(self):
    allocator = InventoryAllocator(
      { 'apple': 1, 'banana': 5 },
      [{ 'name': 'owd', 'inventory': { 'apple': 1, 'banana': 5 } }]
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      [{ 'owd': { 'apple': 1, 'banana': 5 }}]
    )

  def test_no_inventory(self):
    allocator = InventoryAllocator(
      { 'apple': 5 },
      [
        { 'name': 'owd', 'inventory': { 'apple': 2, 'banana': 0 } },
        { 'name': 'dw', 'inventory': { 'apple': 0, 'banana': 10 } },
      ]
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      []
    )

  def test_split_shipment_single_item(self):
    allocator = InventoryAllocator(
      { 'apple': 10 },
      [
        { 'name': 'dm', 'inventory': { 'apple': 5 } },
        { 'name': 'owd', 'inventory': { 'apple': 5 }}
      ]
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      [{ 'dm': { 'apple': 5 }}, { 'owd': { 'apple': 5 } }]
    )

  def test_split_shipment_multiple_items(self):
    allocator = InventoryAllocator(
      { 'apple': 10, 'banana': 2, 'orange': 5 },
      [
        { 'name': 'dm', 'inventory': { 'apple': 5, 'banana': 2 } },
        { 'name': 'owd', 'inventory': { 'apple': 5, 'banana': 2, 'orange': 5 } }
      ]
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      [
        { 'dm': { 'apple': 5, 'banana': 2 }},
        { 'owd': { 'apple': 5, 'orange': 5 } }
      ]
    )

  def test_single_shipment_prioritizes_split_shipment(self):
    allocator = InventoryAllocator(
      { 'apple': 10 },
      [
        { 'name': 'owd', 'inventory': { 'apple': 5 } },
        { 'name': 'dm', 'inventory': { 'apple': 5 } },
        { 'name': 'af', 'inventory': { 'apple': 10 } }
      ]
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      [{ 'af': { 'apple': 10 }}]
    )

  def test_sanitized_inputs(self):
    allocator = InventoryAllocator(
      { 'apple': 0, 'banana': 1 },
      [{ 'name': 'owd', 'inventory': { 'banana': 1 } }]
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      [{ 'owd': { 'banana': 1 }}]
    )

  def test_empty_order(self):
    allocator = InventoryAllocator(
      {},
      [{ 'name': 'owd', 'inventory': { 'banana': 1 } }]
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      []
    )

  def test_empty_warehouses(self):
    allocator = InventoryAllocator(
      { 'banana': 1 },
      []
    )

    self.assertListEqual(
      allocator.calculate_shipments(),
      []
    )


if __name__ == '__main__':
  unittest.main()
