from fpdf import FPDF
# from datetime import date
from datetime import date

class create_pdf:
    
    def __init__(self, output_file_name, patient_name, patient_age, patient_mobile, patient_gender, left_img_path, right_img_path):
        self.pdf = FPDF()
        self.output_file_name = output_file_name
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.patient_mobile = patient_mobile
        self.patient_gender = patient_gender
        self.left_img_path = left_img_path
        self.right_img_path = right_img_path
    
    def build_pdf(self, categories_left, categories_right):

        self.pdf.add_page()

        self.pdf.set_font("Arial", 'UB', size = 35)
        self.pdf.cell(w = 200, h = 20, txt = 'Medical Report', ln = 1, align = 'C', fill = False)
        self.pdf.ln(10)

        self.pdf.set_font("Arial", 'B', size = 15)
        self.pdf.cell(w = 20, h = 10, txt = 'Date : ', ln = 0, align = 'left', fill = False)

        str1 = str(date.today())
        self.pdf.set_font("Arial", size = 15)
        self.pdf.cell(w = 20, h = 10, txt = str1, ln = 1, align = 'left', fill = False)

        self.pdf.set_font("Arial", 'B', size = 15)
        self.pdf.cell(w = 20, h = 10, txt = 'Name : ', ln = 0, align = 'left', fill = False)

        self.pdf.set_font("Arial", size = 15)
        self.pdf.cell(w = 20, h = 10, txt = self.patient_name, ln = 1, align = 'left', fill = False)

        self.pdf.set_font("Arial", 'B', size = 15)
        self.pdf.cell(w = 20, h = 10, txt = 'Age : ', ln = 0, align = 'L', fill = False)

        self.pdf.set_font("Arial", size = 15)
        self.pdf.cell(w = 20, h = 10, txt = self.patient_age, ln = 1, align = 'L', fill = False)

        self.pdf.set_font("Arial", 'B', size = 15)
        self.pdf.cell(w = 45, h = 10, txt = 'Mobile Number : ', ln = 0)

        self.pdf.set_font("Arial", size = 15)
        self.pdf.cell(w = 20, h = 10, txt = self.patient_mobile, ln = 1)

        self.pdf.set_font("Arial", 'B', size = 15)
        self.pdf.cell(w = 25, h = 10, txt = 'Gender : ', ln = 0, align = 'L', fill = False)

        self.pdf.set_font('Arial', size = 15)
        self.pdf.cell(w = 20, h = 10, txt = self.patient_gender, ln = 1)

        self.pdf.ln(20)
        counter = 4

        self.pdf.cell(w = 60, h = 10, txt = '', ln = 0, border = True)
        self.pdf.set_font("Arial", 'B', size = 15)
        self.pdf.cell(w = 60, h = 10, txt = 'Left Eye', ln = 0, border = True)

        self.pdf.set_font("Arial", 'B', size = 15)
        self.pdf.cell(w = 60, h = 10, txt = 'Right Eye', ln = 1, border = True)

        if categories_left['dr'] != -1:
            counter -= 1
            self.pdf.set_font("Arial", 'B', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = 'Diabetic Retinopathy', ln = 0, border = True)

            str5 = str(categories_left['dr'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str5, ln = 0, border = True)

            str6 = str(categories_right['dr'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str6, ln = 1, border = True)

        if categories_left['amd'] != -1:
            counter -= 1
            self.pdf.set_font("Arial", 'B', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = 'Macular Degeneration', ln = 0, border = True)

            str5 = str(categories_left['amd'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str5, ln = 0, border = True)

            str6 = str(categories_right['amd'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str6, ln = 1, border = True)

        if categories_left['cataract'] != -1:
            counter -= 1
            self.pdf.set_font("Arial", 'B', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = 'Cataract', ln = 0, border = True)

            str5 = str(categories_left['cataract'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str5, ln = 0, border = True)

            str6 = str(categories_right['cataract'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str6, ln = 1, border = True)

        if categories_left['glaucoma'] != -1:
            counter -= 1
            self.pdf.set_font("Arial", 'B', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = 'Glaucoma', ln = 0, border = True)

            str5 = str(categories_left['glaucoma'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str5, ln = 0, border = True)

            str6 = str(categories_right['glaucoma'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str6, ln = 1, border = True)


        break_amount = 180 - (counter * 10)

        self.pdf.image(self.left_img_path, x = 20, y = break_amount, w = 80, h = 60)
        self.pdf.image(self.right_img_path, x = 110, y = break_amount, w = 80, h = 60)

        self.pdf.ln(90)
        self.pdf.cell(30)
        self.pdf.set_font('Arial', 'UB', size = 15)
        self.pdf.cell(w = 40, h = 10, txt = 'Left Eye', ln = 0, align = 'C')

        self.pdf.cell(50)
        self.pdf.set_font('Arial', 'UB', size = 15)
        self.pdf.cell(w = 40, h = 10, txt = 'Right Eye', ln = 1, align = 'C')
        self.pdf.output(self.output_file_name)