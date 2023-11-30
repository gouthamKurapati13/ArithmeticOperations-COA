from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

global steps
global title
global vals

steps=[]
title=""
vals = [0, 0, 0]

def decimal_to_binary(decimal, num_bits):
    if decimal < 0:
        sign_bit = '1'
        decimal = abs(decimal)
    else:
        sign_bit = '0'
    binary_string = bin(decimal)[2:].zfill(num_bits)
    return sign_bit + binary_string

def add(binary1, binary2, include_zero=False):
    max_length = max(len(binary1), len(binary2))
    binary1 = '0' * (max_length - len(binary1)) + binary1
    binary2 = '0' * (max_length - len(binary2)) + binary2
    carry = 0
    result = ''
    for i in range(max_length - 1, -1, -1):
        bit_sum = int(binary1[i]) + int(binary2[i]) + carry
        result = str(bit_sum % 2) + result
        carry = bit_sum // 2
    print("***", carry)
    if carry==1:
        result = '1' + result
    elif include_zero:
        result = '0' + result
    return result

def complement(binary):
    cmplt = ''.join('1' if bit == '0' else '0' for bit in binary)
    return cmplt

def xor(binary1, binary2):
    max_length = max(len(binary1), len(binary2))
    binary1 = '0' * (max_length - len(binary1)) + binary1
    binary2 = '0' * (max_length - len(binary2)) + binary2
    result = ''
    for i in range(max_length):
        if binary1[i] != binary2[i]:
            result += '1'
        else:
            result += '0'
    return result


def signed_magnitude_addition(n, A, B):
    global steps
    global title
    title = "Signed Magnitude Addition"
    As = 1 if (A<0) else 0
    Bs = 1 if (B<0) else 0
    steps = []
    A = decimal_to_binary(A, n)
    B = decimal_to_binary(B, n)
    if (len(A) > n+1) or (len(B) > n+1) :
        steps.append(" ".join(("Insufficient bits to represent Augend or Addend", )))
    else:
        As, A = A[0], A[1:]
        Bs, B = B[0], B[1:]
        steps.append("Augend in A")
        steps.append("Addend in B")
        steps.append(" ".join(("As =", As, " A =", A)))
        steps.append(" ".join(("Bs =", Bs, " B =", B)))
        opn = xor(As, Bs)
        steps.append(" ".join(("As xor Bs =", opn)))
        if opn=="0":
            EA = add(A, B, include_zero=True)
            steps.append(" ".join(("EA <-- A+B ==> EA =", EA)))
            E = EA[0]
            A = EA[1:]
            AVF = E
            steps.append(" ".join(("AVF <-- E ==> AVF =", AVF)))
            if AVF=='1':
                steps.append(" ".join(("Since AVF=1,", )))
                steps.append(" ".join(("There is an overflow in result...", )))
            else:
                steps.append(" ".join(("Result = As A =", As, A)))
        else:
            EA = add(add(A, complement(B)), "1", include_zero=True)
            steps.append(" ".join(("EA <-- A+B'+1 ==> EA =", EA)))
            AVF = 0
            steps.append(" ".join(("AVF <-- 0", )))
            E = EA[0]
            A = EA[1:]
            if E=='0':
                steps.append(" ".join(("Since E=0,", )))
                A = complement(A)
                steps.append(" ".join(("A <-- A' ==> A =", A)))
                A = add(A, "1")
                steps.append(" ".join(("A <-- A+1 ==> A =", A)))
                As = complement(As)
                steps.append(" ".join(("As <-- As' ==> As =", As)))
            else:
                if A=="0":
                    As = 0
                    steps.append(" ".join(("As <-- 0 ==> As =", As)))
            steps.append(" ".join(("Result = As A =", As, A)))

def signed_magnitude_subtraction(n, A, B):
    global steps
    global title
    title = "Signed Magnitude Subtraction"
    As = 1 if (A<0) else 0
    Bs = 1 if (B<0) else 0
    steps = []
    A = decimal_to_binary(A, n)
    B = decimal_to_binary(B, n)
    if (len(A) > n+1) or (len(B) > n+1) :
        steps.append(" ".join(("Insufficient bits to represent Minuend or Subtrahend",)))
    else:
        As, A = A[0], A[1:]
        Bs, B = B[0], B[1:]
        steps.append("Minuend in A")
        steps.append("Subtrahend in B")
        steps.append(" ".join(("As =", As, " A =", A)))
        steps.append(" ".join(("Bs =", Bs, " B =", B)))
        opn = xor(As, Bs)    #XOR Operation
        steps.append(" ".join(("As xor Bs =", opn)))
        if opn=="0":
            EA = add(add(A, complement(B), include_zero=True), "1")
            steps.append(" ".join(("EA <-- A+B'+1 ==> EA =", EA)))
            AVF = 0
            steps.append(" ".join(("AVF <-- 0", )))
            E = EA[0]
            A = EA[1:]
            if E=='0':
                steps.append(" ".join(("Since E=0,", )))
                A = complement(A)
                steps.append(" ".join(("A <-- A' ==> A =", A)))
                A = add(A, "1")
                steps.append(" ".join(("A <-- A+1 ==> A =", A)))
                As = complement(As)
                steps.append(" ".join(("As <-- As' ==> As =", As)))
            else:
                if A=="0":
                    As = 0
                    steps.append(" ".join(("As <-- 0 ==> As =", As)))
            steps.append(" ".join(("Result = As A =", As, A)))
        else:
            EA = add(A, B, include_zero=True)
            steps.append(" ".join(("EA <-- A+B ==> EA =", EA)))
            E = EA[0]
            A = EA[1:]
            AVF = E
            steps.append(" ".join(("AVF <-- E ==> AVF =", AVF)))
            if AVF=='1':
                steps.append(" ".join(("Since AVF=1,", )))
                steps.append(" ".join(("There is an overflow in result...", )))
            else:
                steps.append(" ".join(("Result = As A =", As, A)))



def two_s_complement_addition(n, A, B):
    global steps
    steps = []
    global title
    title = "2's COMPLEMENT ADDITION"
    bin1 = decimal_to_binary(A,n)
    bin2 = decimal_to_binary(B,n)
    if(len(bin1) > n+1) or (len(bin2) > n+1) :
        steps.append(" ".join(("Insufficient bits to represent Augend or Addend", )))
    else : 
        if(A < 0) :
            A = add(bin1[0]+complement(bin1[1:]),"1")
        else :
            A = bin1
        if(B < 0) :
            B = add(bin2[0]+complement(bin2[1:]),"1")
        else :
            B = bin2
        result = add(A,B,include_zero=True)
        overflow = xor(xor(xor(A[0],B[0]),result[1]),result[0])
        steps.append(" ".join(("Augend ---> ",A)))
        steps.append(" ".join(("Addend ---> ",B)))
        steps.append(" ".join(("Overflow ---> ",overflow)))
        if(overflow == "0") :
            steps.append(" ".join(("Result ---> ",result[1:])))
            if(result[1] == "1") :
                steps.append(" ".join(("2's Complement of Result --->",add(result[0]+complement(result[1:]),"1")[1:])))
    

def two_s_complement_subtraction(n, A, B):
    global steps
    steps = []
    global title
    title = "2's COMPLEMENT SUBTRACTION"
    bin1 = decimal_to_binary(A,n)
    bin2 = decimal_to_binary(B,n)
    if(len(bin1) > n+1) or (len(bin2) > n+1) :
        steps.append(" ".join(("Insufficient bits to represent Minuend or Subtrahend", )))
    else :
        if(A < 0) :
            A = add(bin1[0]+complement(bin1[1:]),"1")
        else :
            A = bin1
        if(B < 0) :
            B = add(bin2[0]+complement(bin2[1:]),"1")
        else :
            B = bin2

        steps.append(" ".join(("Minuend ---> ",A)))
        steps.append(" ".join(("Subtrahend ---> ",B)))
        B = add(complement(B),"1")
        result = add(A,B,include_zero=True)
        overflow = xor(xor(xor(A[0],B[0]),result[1]),result[0])
        steps.append(" ".join(("Overflow ---> ",overflow)))
        if(overflow == "0") :
            steps.append(" ".join(("Result ---> ",result[1:])))
            if(result[1] == "1") :
                steps.append(" ".join(("2's Complement of Result --->",add(result[0]+complement(result[1:]),"1")[1:])))


@app.route('/')
def index():
    return render_template('index.html', steps=steps, title=title, vals=vals)


@app.route('/perform_operation', methods=['POST'])
def perform_operation():
    global vals
    n = int(request.form.get('bits'))
    A = int(request.form.get('num1'))
    B = int(request.form.get('num2'))
    vals = [n, A, B]
    opn = request.form.get('operation')
    if (opn == 'Add 1'):
        signed_magnitude_addition(n, A, B)
    elif (opn == 'Sub 1'):
        signed_magnitude_subtraction(n, A, B)
    elif (opn == 'Add 2'):
        two_s_complement_addition(n, A, B)
    elif (opn == 'Sub 2'):
        two_s_complement_subtraction(n,A,B)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)