from django import template
register=template.Library()

@register.filter
def W(W1,W2):
    if W1==0 and W2==0:
        value = "经验不限"
    elif W2==100:
        value="%r年以上"%W1
    else:
        value="%r~%r年"%(W1,W2)
    return value

@register.filter
def K(K1,K2):
    K1=int(K1)
    K2=int(K2)
    value = "%dK~%dK"%(K1,K2)
    if K2 == 0 and K2==0:
        value = "薪资面议"
    return value
