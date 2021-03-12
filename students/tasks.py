from celery import shared_task
from sheet_engine.functions import generate_record_sheet


@shared_task(bind=True)
def generate_record_sheet_task(self, task_id):
	set_task_state(self, "EXTRACTING PAGES", 1, total=2)
	for page, image in enumerate(images):
		absolute_file_path = image.file.file
		pdf = pytesseract.image_to_pdf_or_hocr(Image.open(absolute_file_path))

		fs = FileSystemStorage()	
		fn = fs.path("temp/"+dir_name)+"/page_"+str(page)+".pdf"
		with open(fn, "wb") as file:
			file.write(pdf)
	
	set_task_state(self, "MERGING PDFS", 2, total=2)
	result_path = merge_pdfs(dir_name, images.count())
	return result_path

def set_task_state(task, message, current, total=5, info=""):
	task.update_state(
		state = message,
		meta = {
			"current": str(current),
			"total"  : total,
			"info"   : info
		}
	)	