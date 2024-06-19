import gspread




def pricegetter(key):
    gc = gspread.service_account(filename='private_key.json')
    sh = gc.open('SwastikJewellery')
    wks = gc.open("SwastikJewellery").sheet1
    code = wks.get('A:A')

    price = wks.get('B:B')
    filename=code[len(code)-1][0]+1
    dict={}
    for i in range(1, len(code)):
        print(code[i][0], price[i][0])
        dict[code[i][0]] = price[i][0]
    return dict[key]


# ans = pricegetter( 'n1')
# print(ans)
# worksheet=sh.worksheet('SwastikJewellery')
# print(gc)
# print(wks.update('A1',[['n1',2],[3,4]]))
# wks.update('B42',"fdhsiv")
# cell=gc.find("n1")
# print(cell.row,cell.col)