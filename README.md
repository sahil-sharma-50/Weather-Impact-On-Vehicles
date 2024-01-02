# Weather-Impact-On-Vehicles Project

This repository contains a data science project on the influence of weather on vehicles type involved in accidents.
Before you begin, make sure you have [Python](https://www.python.org/) installed. We will work with [Jupyter notebooks](https://jupyter.org/). The easiest way to do so is to set up [VSCode](https://code.visualstudio.com/) with the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter).


## Project Work: Analyze different weather conditions and their impact on different types of vehicles involved in road accidents.
This project aims to figure out how weather influences road safety, especially if the weather conditions affect the types of vehicles involved in an accident, which is super important for creating better safety rules. It checks out how different weather conditions relate to the number of accidents. It looks at accident data from Berlin to see how these weather conditions impact the number of accidents.<br><br>
This project aims to investigate the following aspects:
<ol>
	<li>Which road condition has the most impact on road accidents?</li>
	<li>Which type of vehicle is most likely to be involved in an accident?</li>
	<li>How do different weather conditions impact the types of vehicles involved in accidents?</li>
	<li>Is there any trend in vehicle accidents over the period of a year?</li>
</ol>

### Project Structure:
`data_pipeline.py`: Main script for data pipeline, responsible for handling and processing data.<br>
`test.py`: Test cases for testing various functionalities of the pipeline, ensuring its correctness and reliability.<br>
`data\accident_data.csv`: Accident dataset in CSV format.<br>
`Report`: Document summarizing the results, findings, or insights derived from the data analysis.<br>
`start_pipeline.sh`: Shell script used to start the data pipeline.<br>
`start_test.sh`:  Shell script used to start the testing process for the project.<br>

### Insights of the Project:
1. **Comprehensive Analysis Report: [report.ipynb](https://github.com/sahil-sharma-50/Weather-Impact-On-Vehicles/blob/master/Report/report.ipynb)**
2. **Presentation Slides: [slides.pdf](https://github.com/sahil-sharma-50/Weather-Impact-On-Vehicles/blob/master/Report/slides.pdf)**

### Exporting a Jupyter Notebook
Jupyter Notebooks can be exported using `nbconvert` (`pip install nbconvert`). For example, to export the example notebook to html: `jupyter nbconvert --to html examples/final-report-example.ipynb --embed-images --output final-report.html`
