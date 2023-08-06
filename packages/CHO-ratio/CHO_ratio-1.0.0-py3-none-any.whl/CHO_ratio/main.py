from struct import pack

ZERO = 0xE28280

def Ratio(CHO, CO2, H2O, str_output=False):
    """
    CHO [mg] : 元の物質の質量
    CO2 [mg] : 塩化カルシウム管の質量の増加分
    H2O [mg] : ソーダ石灰管の質量の増加分
    """

    C = CO2 * (12 / 44)
    H = H2O * ( 2 / 18)
    O = CHO - (C + H)

    Cmmol = C / 12
    Hmmol = H /  1
    Ommol = O / 16

    minimum = min([Cmmol, Hmmol, Ommol])
    Cn = int(Cmmol / minimum)
    Hn = int(Hmmol / minimum)
    On = int(Ommol / minimum)

    if str_output:
        return f"C{pack('>I', ZERO+Cn)[1:].decode()}H{pack('>I', ZERO+Hn)[1:].decode()}O{pack('>I', ZERO+On)[1:].decode()}"
    else:
        return Cn, Hn, On

