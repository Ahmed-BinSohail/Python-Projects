
print("========== ELECTRICITY BILL CALCULATOR ==========")

name = input("Enter customer name: ")

customer_type = input("Enter customer type (R for Residential / C for Commercial): ")
customer_type = customer_type.upper()

previous_reading = int(input("Enter previous meter reading: "))
current_reading = int(input("Enter current meter reading: "))

paid_late = input("Was the bill paid after the due date? (Y/N): ")
paid_late = paid_late.upper()

if customer_type != "R" and customer_type != "C":
    print("Error: Invalid customer type. Enter R or C.")

elif previous_reading < 0 or current_reading < 0:
    print("Error: Meter readings cannot be negative.")

elif current_reading < previous_reading:
    print("Error: Current reading cannot be less than previous reading.")

else:
    units = current_reading - previous_reading

    if customer_type == "R":

        if units <= 100:
            energy = units * 10

        elif units <= 200:
            energy = (100 * 10) + ((units - 100) * 15)

        elif units <= 300:
            energy = (100 * 10) + (100 * 15) + ((units - 200) * 20)

        else:
            energy = (100 * 10) + (100 * 15) + (100 * 20) + ((units - 300) * 25)

        if units <= 200:
            fixed = 100
        else:
            fixed = 200

    else:
        energy = units * 30
        fixed = 500

    gst = (energy + fixed) * 0.18

    if paid_late == "Y":
        surcharge = (energy + fixed + gst) * 0.10
    else:
        surcharge = 0

    total = energy + fixed + gst + surcharge

    if units <= 100:
        level = "Low"

    elif units <= 300:
        level = "Moderate"

    else:
        level = "High"

    if customer_type == "R":
        type_name = "Residential"
    else:
        type_name = "Commercial"

    print("\n============== ITEMIZED ELECTRICITY BILL ==============")

    print("Customer Name:             ", name)
    print("Customer Type:             ", type_name)
    print("Previous Meter Reading:    ", previous_reading)
    print("Current Meter Reading:     ", current_reading)
    print("Units Consumed:             ", units)

    print("Energy Charges:             Rs.", format(energy, ".2f"))
    print("Fixed Charges:              Rs.", format(fixed, ".2f"))
    print("GST (18%):                  Rs.", format(gst, ".2f"))
    print("Late Payment Surcharge:     Rs.", format(surcharge, ".2f"))

    print("Total Payable:              Rs.", format(total, ".2f"))
    print("Consumption Level:         ", level)

    print("=======================================================")
