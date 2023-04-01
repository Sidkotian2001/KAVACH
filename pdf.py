from fpdf import FPDF
# from datetime import date
from datetime import date

class create_pdf:
    
    def __init__(self, output_file_name, time, threat_class, threat_level, location):
        self.pdf = FPDF()
        self.output_file_name = output_file_name
        self.time = time
        self.threat_class = threat_class
        self.threat_level = threat_level
        self.location = location

    
    def build_pdf(self):

        self.pdf.add_page()

        self.pdf.set_font("Arial", 'UB', size = 35)
        self.pdf.cell(w = 200, h = 20, txt = 'Crime Report', ln = 1, align = 'C', fill = False)
        self.pdf.ln(10)

        self.pdf.set_font("Arial", 'B', size = 25)
        self.pdf.cell(w = 30, h = 10, txt = 'Date : ', ln = 0, align = 'left', fill = False)

        str1 = str(date.today())
        self.pdf.set_font("Arial", size = 25)
        self.pdf.cell(w = 20, h = 10, txt = self.time, ln = 1, align = 'right', fill = False)

        self.pdf.set_font("Arial", 'B', size = 25)
        self.pdf.cell(w = 60, h = 10, txt = 'Threat Class : ', ln = 0, align = 'left', fill = False)

        self.pdf.set_font("Arial", size = 25)
        self.pdf.cell(w = 20, h = 10, txt = self.threat_class, ln = 1, align = 'right', fill = False)

        self.pdf.set_font("Arial", 'B', size = 25)
        self.pdf.cell(w = 60, h = 10, txt = 'Threat Level : ', ln = 0, align = 'L', fill = False)

        self.pdf.set_font("Arial", size = 25)
        self.pdf.cell(w = 20, h = 10, txt = self.threat_level, ln = 1, align = 'R', fill = False)

        self.pdf.set_font("Arial", 'B', size = 25)
        self.pdf.cell(w = 50, h = 10, txt = 'Location : ', ln = 0)

        self.pdf.set_font("Arial", size = 25)
        self.pdf.cell(w = 20, h = 10, txt = self.location, ln = 1)


        # self.pdf.ln(20)
        # counter = 4

        # self.pdf.cell(w = 60, h = 10, txt = '', ln = 0, border = True)
        # self.pdf.set_font("Arial", 'B', size = 15)
        # self.pdf.cell(w = 60, h = 10, txt = 'Left Eye', ln = 0, border = True)

        # self.pdf.set_font("Arial", 'B', size = 15)
        # self.pdf.cell(w = 60, h = 10, txt = 'Right Eye', ln = 1, border = True)

        # if categories_left['dr'] != -1:
        #     counter -= 1
        #     self.pdf.set_font("Arial", 'B', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = 'Diabetic Retinopathy', ln = 0, border = True)

        #     str5 = str(categories_left['dr'])
        #     self.pdf.set_font('Arial', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = str5, ln = 0, border = True)

        #     str6 = str(categories_right['dr'])
        #     self.pdf.set_font('Arial', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = str6, ln = 1, border = True)

        # if categories_left['amd'] != -1:
        #     counter -= 1
        #     self.pdf.set_font("Arial", 'B', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = 'Macular Degeneration', ln = 0, border = True)

        #     str5 = str(categories_left['amd'])
        #     self.pdf.set_font('Arial', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = str5, ln = 0, border = True)

        #     str6 = str(categories_right['amd'])
        #     self.pdf.set_font('Arial', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = str6, ln = 1, border = True)

        # if categories_left['cataract'] != -1:
        #     counter -= 1
        #     self.pdf.set_font("Arial", 'B', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = 'Cataract', ln = 0, border = True)

        #     str5 = str(categories_left['cataract'])
        #     self.pdf.set_font('Arial', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = str5, ln = 0, border = True)

        #     str6 = str(categories_right['cataract'])
        #     self.pdf.set_font('Arial', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = str6, ln = 1, border = True)

        # if categories_left['glaucoma'] != -1:
        #     counter -= 1
        #     self.pdf.set_font("Arial", 'B', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = 'Glaucoma', ln = 0, border = True)

        #     str5 = str(categories_left['glaucoma'])
        #     self.pdf.set_font('Arial', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = str5, ln = 0, border = True)

        #     str6 = str(categories_right['glaucoma'])
        #     self.pdf.set_font('Arial', size = 15)
        #     self.pdf.cell(w = 60, h = 10, txt = str6, ln = 1, border = True)


        # break_amount = 180 - (counter * 10)

        # self.pdf.image(self.left_img_path, x = 20, y = break_amount, w = 80, h = 60)
        # self.pdf.image(self.right_img_path, x = 110, y = break_amount, w = 80, h = 60)

        # self.pdf.ln(90)
        # self.pdf.cell(30)
        # self.pdf.set_font('Arial', 'UB', size = 15)
        # self.pdf.cell(w = 40, h = 10, txt = 'Left Eye', ln = 0, align = 'C')

        # self.pdf.cell(50)
        # self.pdf.set_font('Arial', 'UB', size = 15)
        # self.pdf.cell(w = 40, h = 10, txt = 'Right Eye', ln = 1, align = 'C')
        self.pdf.output(self.output_file_name)