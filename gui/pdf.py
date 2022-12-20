from fpdf import FPDF

pdf = FPDF()
pdf.add_page()




pdf.set_font("Arial", 'UB', size = 35)
pdf.cell(w = 200, h = 20, txt = 'Medical Report', ln = 1, align = 'C', fill = False)
pdf.ln(10)

pdf.set_font("Arial", 'B', size = 15)
pdf.cell(w = 20, h = 10, txt = 'Date : ', ln = 0, align = 'left', fill = False)

str1 = '21/12/2022'
pdf.set_font("Arial", size = 15)
pdf.cell(w = 20, h = 10, txt = str1, ln = 1, align = 'left', fill = False)

pdf.set_font("Arial", 'B', size = 15)
pdf.cell(w = 20, h = 10, txt = 'Name : ', ln = 0, align = 'left', fill = False)

str1 = 'Siddharth Kotian'
pdf.set_font("Arial", size = 15)
pdf.cell(w = 20, h = 10, txt = str1, ln = 1, align = 'left', fill = False)

pdf.set_font("Arial", 'B', size = 15)
pdf.cell(w = 20, h = 10, txt = 'Age : ', ln = 0, align = 'L', fill = False)

str2 = '21'
pdf.set_font("Arial", size = 15)
pdf.cell(w = 20, h = 10, txt = str2, ln = 1, align = 'L', fill = False)

pdf.set_font("Arial", 'B', size = 15)
pdf.cell(w = 45, h = 10, txt = 'Mobile Number : ', ln = 0)

str3 = '9619616979'
pdf.set_font("Arial", size = 15)
pdf.cell(w = 20, h = 10, txt = str3, ln = 1)

pdf.set_font("Arial", 'B', size = 15)
pdf.cell(w = 25, h = 10, txt = 'Gender : ', ln = 0, align = 'L', fill = False)

str4 = 'Male'
pdf.set_font('Arial', size = 15)
pdf.cell(w = 20, h = 10, txt = str4, ln = 1)

Dr = True
Md = True
Cat = True
Gla = True

pdf.ln(20)

counter = 4

pdf.set_font("Arial", 'B', size = 15)
pdf.cell(w = 60, h = 10, txt = 'Disease', ln = 0, border = True, align = 'C')

pdf.set_font("Arial", 'B', size = 15)
pdf.cell(w = 40, h = 10, txt = 'Condition', ln = 1, border = True, align = 'C')



if Dr :
    counter -= 1
    pdf.set_font("Arial", 'B', size = 15)
    pdf.cell(w = 60, h = 10, txt = 'Diabetic Retinopathy', ln = 0, border = True)

    str5 = 'Yes'
    pdf.set_font('Arial', size = 15)
    pdf.cell(w = 40, h = 10, txt = str5, ln = 1, border = True)

if Md :
    counter -= 1
    pdf.set_font("Arial", 'B', size = 15)
    pdf.cell(w = 60, h = 10, txt = 'Macular Degeneration', ln = 0, border = True)

    str5 = 'Yes'
    pdf.set_font('Arial', size = 15)
    pdf.cell(w = 40, h = 10, txt = str5, ln = 1, border = True)

if Cat :
    counter -= 1
    pdf.set_font("Arial", 'B', size = 15)
    pdf.cell(w = 60, h = 10, txt = 'Cataract', ln = 0, border = True)

    str5 = 'Yes'
    pdf.set_font('Arial', size = 15)
    pdf.cell(w = 40, h = 10, txt = str5, ln = 1, border = True)

if Gla :
    counter -= 1
    pdf.set_font("Arial", 'B', size = 15)
    pdf.cell(w = 60, h = 10, txt = 'Glaucoma', ln = 0, border = True)

    str5 = 'Yes'
    pdf.set_font('Arial', size = 15)
    pdf.cell(w = 40, h = 10, txt = str5, ln = 1, border = True)



break_amount = 180 - (counter * 10)

pdf.image('image_taken_0.jpg', x = 20, y = break_amount, w = 80, h = 60)
pdf.image('image_taken_1.jpg', x = 110, y = break_amount, w = 80, h = 60)

pdf.ln(87)
pdf.cell(30)
pdf.set_font('Arial', 'UB', size = 15)
pdf.cell(w = 40, h = 10, txt = 'Left Eye', ln = 0, align = 'C')

pdf.cell(50)
pdf.set_font('Arial', 'UB', size = 15)
pdf.cell(w = 40, h = 10, txt = 'Right Eye', ln = 1, align = 'C')

pdf.output('trial.pdf')