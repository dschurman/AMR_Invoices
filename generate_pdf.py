# adapted from https://www.blog.pythonlibrary.org/2012/07/10/an-intro-to-pyfpdf-a-simple-python-pdf-generation-library/
import fpdf
import requests
import sys

########################################################################
class MyPDF(fpdf.FPDF):
    """"""
    def header(self):
        # set the font for the header, B=Bold
        self.set_font("Times", style="B", size=18)
        # page title
        self.cell(100,10, "Fairfield Warehouse Rent Invoice", border=1, ln=0, align="C")
        # insert a line break of 20 pixels
        self.ln(20)
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    pdf = MyPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Times", size=12)

    for name in sys.argv[1:]:
    	params = {'query':'true', 'name':name}
    	resp = requests.get('https://script.google.com/a/brown.edu/macros/s/AKfycbyqAzt_4jFCGJRxPePAlv39t5-Mmfwr3F4LdCg1rLjcato-HdYV/exec', params=params)
    	resp = resp.json()
    	total = resp['amt']
    	month_cons = resp['month_cons']
    	pow_rate = resp['pow_rate']
    	rent = resp['rent']

    	pdf.cell(50, 10, 'Amount Due: $' + str(total), border=1)
    	pdf.ln(20)
    	pdf.cell(0, 10, 'This month, you used a total of ' + str(month_cons) + ' kilowatt-hours (kWh) of electricity.', border=0, ln=1)
    	pdf.cell(0, 10, 'At a rate of $' + str(pow_rate) + ' per kWh, your power usage total amounts to ' + str(float(pow_rate) * int(month_cons)) + '$', border=0, ln=1)
    	pdf.cell(0, 10, 'Your monthly rent rate is $' + str(rent), border=0, ln=1)

    	pdf.output(name + '_' + resp['date'] + '.pdf')