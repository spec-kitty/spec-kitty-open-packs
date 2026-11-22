# Worked example: unfaking an over-mocked test (order fulfilment)

This example walks the procedure `unfake-an-over-mocked-test` on one test, from the over-mocked original to a test that runs the owned logic for real. The domain is neutral: an order-fulfilment service.

## The original test

The service under test ships paid orders. For each order it reserves stock, records a shipment, and calls the carrier. A later step, the dispatch report, reads the recorded shipments.

```python
def test_ship_paid_orders(monkeypatch):
    recorded = []
    monkeypatch.setattr(fulfilment, "_record_shipment", lambda order: recorded.append(order.id))
    monkeypatch.setattr(fulfilment, "_reserve_stock", lambda order: None)
    monkeypatch.setattr(carrier_client, "book", lambda shipment: "TRACK-1")

    fulfilment.ship_paid_orders(store, [order_a, order_b])

    assert recorded == ["A-1", "A-2"]          # pins a call contract on owned logic
    report = dispatch_report(store)
    assert report.lines == 2                    # fails: no shipment was ever stored
```

The second assertion failed. The failure looked like data loss: "shipments recorded, but the report is empty". It was not. The stub of `_record_shipment` wrote nothing, so the store held no shipment, a state the real code never produces. The investigation chased a state only the stub could create.

## Step 1: Name the behaviour under test

"Shipping paid orders stores one shipment per order, and the dispatch report lists them." The behaviour, not the function `_record_shipment`.

## Step 2: Draw the responsibility boundary

Inside: `ship_paid_orders`, stock reservation, shipment recording, the store's write path, the dispatch report. Outside: the carrier, a separate company reached over the network.

## Step 3: Classify each double

| Double | Seam | Verdict |
|--------|------|---------|
| `_record_shipment` | owned logic | remove |
| `_reserve_stock` | owned logic | remove |
| `carrier_client.book` | network to an external service | keep |

## Step 4: Run the real collaborators on realistic seeded state

Create the orders through the real order pipeline (place and pay them) instead of building records by hand, so only reachable states exist. Stock one book and one lamp first, because stock reservation now runs for real. The carrier is now passed in as a parameter instead of patched at module level, so the one remaining substitute is visible at the call.

## Step 5: Move assertions from calls to outcomes

```python
def test_shipping_paid_orders_stores_one_shipment_per_order(fake_carrier):
    store = Store.in_temp_dir()
    stock(store, book=1, lamp=1)
    order_a = place_and_pay(store, items=["book"])
    order_b = place_and_pay(store, items=["lamp"])

    fulfilment.ship_paid_orders(store, [order_a, order_b], carrier=fake_carrier)

    shipments = store.shipments()
    assert sorted(s.order_id for s in shipments) == sorted([order_a.id, order_b.id])
    assert dispatch_report(store).lines == 2
```

## Step 6: Check the remaining substitute

`fake_carrier` keeps the carrier's contract: it returns a tracking number for a valid shipment and raises the carrier's own error for an unknown address. A fake that always succeeded would hide the failure branch, moving the anti-pattern one step out.

## Step 7: Prove the test is not vacuous

Break the behaviour (make the recording step skip the second order), watch the test fail on the missing second order id, record that failure text, and restore the code.

## Step 8: Budget the cost

The new test needs a temporary store and the order pipeline. If that setup grows heavy, extract a pure seam (for example a function that turns paid orders into shipment records) and test it with plain inputs, as `test-scaffolding-as-design-smell` describes.

## What changed

- Before: the test pinned which helper was called and could manufacture an impossible state.
- After: owned logic runs for real, only the external carrier is substituted, and the assertions read the stored outcome.
