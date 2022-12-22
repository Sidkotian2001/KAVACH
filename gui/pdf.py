from fpdf import FPDF
# from datetime import date

class create_pdf:
    
    def __init__(self, output_file_name, patient_name, patient_age, patient_mobile, patient_gender):
        self.pdf = FPDF()
        self.output_file_name = output_file_name
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.patient_mobile = patient_mobile
        self.patient_gender = patient_gender
    
    def build_pdf(self, categories):

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

        if categories['DIABETIC RETINOPATHY'] != -1:
            counter -= 1
            self.pdf.set_font("Arial", 'B', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = 'Diabetic Retinopathy', ln = 0, border = True)

            str5 = str(categories['DIABETIC RETINOPATHY'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str5, ln = 1, border = True)

        if categories['Macular Degeneration'] != -1:
            counter -= 1
            self.pdf.set_font("Arial", 'B', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = 'Macular Degeneration', ln = 0, border = True)

            str5 = str(categories['Macular Degeneration'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str5, ln = 1, border = True)

        if categories['CATARACT'] != -1:
            counter -= 1
            self.pdf.set_font("Arial", 'B', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = 'Cataract', ln = 0, border = True)

            str5 = str(categories['CATARACT'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str5, ln = 1, border = True)

        if categories['Glucama'] != -1:
            counter -= 1
            self.pdf.set_font("Arial", 'B', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = 'Glaucoma', ln = 0, border = True)

            str5 = str(categories['Glucama'])
            self.pdf.set_font('Arial', size = 15)
            self.pdf.cell(w = 60, h = 10, txt = str5, ln = 1, border = True)


        break_amount = 180 - (counter * 10)

        self.pdf.image('image_taken_0.jpg', x = 20, y = break_amount, w = 80, h = 60)
        self.pdf.image('image_taken_1.jpg', x = 110, y = break_amount, w = 80, h = 60)

        self.pdf.ln(90)
        self.pdf.cell(30)
        self.pdf.set_font('Arial', 'UB', size = 15)
        self.pdf.cell(w = 40, h = 10, txt = 'Left Eye', ln = 0, align = 'C')

        self.pdf.cell(50)
        self.pdf.set_font('Arial', 'UB', size = 15)
        self.pdf.cell(w = 40, h = 10, txt = 'Right Eye', ln = 1, align = 'C')
        self.pdf.output(self.output_file_name)