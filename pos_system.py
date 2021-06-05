import pandas as pd
import sys
import datetime

ITEM_MASTER_CSV_PATH="./item_master.csv"
RECEIPT_FOLDER="./receipt"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        self.set_datetime()
        
    def set_datetime(self):
        self.datetime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    def add_item_order(self,item_code,item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)
        
    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))
            
    # オーダー番号から商品情報を取得する
    def get_item_data(self,item_code):
        for m in self.item_master:
            if item_code == m.item_code:
                return m.item_name,m.price
    
    # オーダー入力
    def input_order(self):
        print("いらっしゃいませ！")
        while True:
            buy_item_code = input("購入したい商品コードを入力してください。終了する場合は、0を入力してください >>> ")
            if int(buy_item_code) != 0:
                item = self.get_item_data(buy_item_code)
                if item!=None:
                    print("{0} ({1}円)が登録されました".format(item[0], item[1]))
                    buy_item_count = input("購入個数を入力してください　>>> ")
                    self.add_item_order(buy_item_code,buy_item_count)
                else:
                    print("「{}」は商品マスタに存在しません".format(buy_item_code))
            else:
                print("商品登録を終了します。")
                break

    def order_detail(self):
        number = 1
        self.sum_price = 0
        self.sum_count = 0
        self.receipt_name = "receipt_{}.log".format(self.datetime)
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("オーダー登録された商品一覧\n")
        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            result = self.get_item_data(item_order)
            self.sum_price += result[1] * int(item_count)
            self.sum_count += int(item_count)
            receipt_data = "{0}.{2}({1}) : ￥{3:,}　{4}個 = ￥{5:,}".format(number, item_order, result[0], result[1], item_count, int(result[1]) * int(item_count))
            self.write_receipt(receipt_data)
            number += 1
            
        # 合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("合計金額:￥{0} {1}個".format(self.sum_price,self.sum_count))
    
    def calc_money(self):
        if len(self.item_order_list) >= 1:
            while True:
                self.money = input("お支払い金額を入力してください >>> ")
                self.change_money = int(self.money) - self.sum_price
                if self.change_money >= 0:
                    self.write_receipt("お預り:￥{}".format(self.money))
                    self.write_receipt("お釣り：￥{}".format(self.change_money))
                    break
                else:
                    print("￥{}　円不足しています。再度入力してください".format(self.change_money))
            
            print("ありがとうございました。")
            
    def write_receipt(self,text):
        print(text)
        with open(RECEIPT_FOLDER + "\\" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n") 
        
### マスタ登録
def regist_item_by_csv(csv_path):
    print("------- マスタ登録開始 ---------")
    item_master = []
    count=0
    try:
        # item_codeの0が落ちるため、dtypeを設定
        item_master_df = pd.read_csv(csv_path,dtype = {"item_code":object})
        for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
            item_master.append(Item(item_code,item_name,price))
            print("{}({})".format(item_name,item_code))
            count+=1
        print("{}品の登録を完了しました。".format(count))
        print("------- マスタ登録完了 ---------")
        return item_master
    except:
        print("マスタ登録が失敗しました")
        print("------- マスタ登録完了 ---------")
        sys.exit()
        

### メイン処理
def main():
    # CSVからマスタへ登録
    item_master=regist_item_by_csv(ITEM_MASTER_CSV_PATH)
    # マスタをオーダーに登録
    order=Order(item_master)
    # オーダー入力
    order.input_order()
    # オーダー番号から商品情報を取得
    order.order_detail()
    order.calc_money()

if __name__ == "__main__":
    main()