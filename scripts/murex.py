from datetime import datetime
import pytz, re


def current_timestamp():
    current_date = datetime.now(pytz.timezone("GMT"))
    return int(current_date.timestamp())


def main(data, ID, goldenContract, cid, account):
    struct_trade = goldenContract.findTrade(ID, "GBO", {"from": account})
    trade = struct_trade[2]
    # print(trade)

    if trade is not None:
        chain_amount_buy_fee = re.search(r"amountBuyFee:(\d+\.\d+)", trade).group(1)
        chain_amount_buy_interest = re.search(r"amountBuyInterest:(\d+\.\d+)", trade).group(1)
        chain_amount_sell_fee = re.search(r"amountSellFee:(\d+\.\d+)", trade).group(1)
        chain_amount_sell_interest = re.search(r"amountSellInterest:(\d+\.\d+)", trade).group(1)

        pc_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"][
            "paymentConvention"
        ]
        pc_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"][
            "paymentConvention"
        ]

        amount_buy_fee = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"][
            "flows"
        ][0]["amount"]
        amount_buy_interest = data["esperanto"]["deals"]["deal1"]["legs"][
            "SELL_Floating"
        ]["flows"][0]["amount"]
        amount_sell_fee = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"][
            "flows"
        ][0]["amount"]
        amount_sell_interest = data["esperanto"]["deals"]["deal1"]["legs"][
            "SELL_Floating"
        ]["flows"][0]["amount"]

        print(
            "\n---Checking on the chain for GBO copy of the Trade and checking if it has changed---"
        )
        flag = True
        # check equality
        if not goldenContract.isEqual(
            amount_buy_fee, chain_amount_buy_fee, {"from": account}
        ):
            print(f"\nOperation Failed: {amount_buy_fee} != {chain_amount_buy_fee}")
            flag = False
        if not goldenContract.isEqual(
            amount_buy_interest, chain_amount_buy_interest, {"from": account}
        ):
            print(
                f"\nOperation Failed: {amount_buy_interest} != {chain_amount_buy_interest}"
            )
            flag = False
        if not goldenContract.isEqual(
            amount_sell_fee, chain_amount_sell_fee, {"from": account}
        ):
            print(f"\nOperation Failed: {amount_sell_fee} != {chain_amount_sell_fee}")
            flag = False
        if not goldenContract.isEqual(
            amount_sell_interest, chain_amount_sell_interest, {"from": account}
        ):
            print(
                f"\nOperation Failed: {amount_sell_interest} != {chain_amount_sell_interest}"
            )
            flag = False

        if flag == False:
            print("\nThe data is not the same as that of the GBO version! ")
            print(f"\nThe CID of the JSON is: {cid}")
            print("------------------------------------------------")
            return 0
        else:
            print("\nThe data is same as that of the GBO version!")
            print("\nAll the rules satisfied! Storing on Blockchain! ")
            print("------------------------------------------------")

            trade1 = f"buyPaymentConvention:{pc_buy}, sellPaymentConvention:{pc_sell}, amountBuyFee:{amount_buy_fee}, amountBuyInterest:{amount_buy_interest}, amountSellFee:{amount_sell_fee}, amountSellInterest:{amount_sell_interest}, jsonCID:{cid}"
            # print(trade)

            ts = current_timestamp()
            t = goldenContract.store(ts, ID, "Murex", trade1, {"from": account})
            t.wait(1)

            print("\nSuccessfully stored the data on the blockchain!!")
            print("\nThe details of the trade as stored on the blockchain:")
            print(goldenContract.trades(ts,{"from": account}))
            return 1
    else:
        print("There is no instance of this trade on the blockchain!!")
        return 0

