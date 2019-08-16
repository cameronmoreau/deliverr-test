from typing import cast, Dict, List, Union

Order = Dict[str, int]
Warehouse = Dict[str, Union[str, Order]]
Shipment = Dict[str, Order]

class InventoryAllocator:
  def __init__(self, order: Order, warehouses: List[Warehouse]):
    self.order = self.__sanitize_order(order)
    self.warehouses = warehouses

  def calculate_shipments(self) -> List[Shipment]:
    # Validate input
    if not self.order or not self.warehouses:
      return list()

    split_checklist = self.order.copy()
    split_shipments: List[Shipment] = list()

    for warehouse in self.warehouses:
      name = cast(str, warehouse['name'])
      inventory = cast(Order, warehouse['inventory'])

      single_checklist = self.order.copy()
      single_shipment_order: Order = dict()
      split_shipment_order: Order = dict()

      for item, amount_needed in self.order.items():
        inventory_amount: int = inventory.get(item, 0)

        if inventory_amount > 0:
          if inventory_amount >= amount_needed:
            single_shipment_order[item] = amount_needed
            del single_checklist[item]

          # Split shipment
          if item in split_checklist:
            split_amount_needed = split_checklist[item]

            if inventory_amount >= split_amount_needed:
              split_shipment_order[item] = split_amount_needed
              del split_checklist[item]
            else:
              split_shipment_order[item] = inventory_amount
              split_checklist[item] -= inventory_amount

      # Full order found
      if not single_checklist:
        return [{ name: single_shipment_order }]

      # Partial order found
      if split_shipment_order:
        split_shipments.append({ name: split_shipment_order })

    # Split shipment fulfilled
    if not split_checklist:
      return split_shipments

    return list()

  def __sanitize_order(self, order: Order) -> Order:
    return dict(filter(lambda o: o[1] > 0, order.items()))
