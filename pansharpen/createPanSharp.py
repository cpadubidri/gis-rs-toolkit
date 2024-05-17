import arcpy
import os
from datetime import datetime
from arcpy.sa import *


def validate_input_paths(*paths):
    """ Check if given file paths exist """
    for path in paths:
        if not arcpy.Exists(path):
            print(f"Error: Path does not exist - {path}")
            return False
        else:
            # print(f"Path validated: {path}")
            pass
    return True



def pansharpen(inpathms, inpathpn, outpath):
    if not validate_input_paths(inpathms, inpathpn):
        return False
    
    if not os.path.exists(os.path.dirname(outpath)):
        print("outpath Not exists")
        return False
    
    try:
        arcpy.management.CreatePansharpenedRasterDataset(
            in_raster=inpathms,
            red_channel="3",     # Specify the correct band number for Red channel
            green_channel="2",   # Specify the correct band number for Green channel
            blue_channel="1",    # Specify the correct band number for Blue channel
            infrared_channel="4", # Specify the correct band number for NIR channel, if not applicable use ""
            out_raster_dataset=outpath,
            in_panchromatic_image=inpathpn,
            pansharpening_type="Gram-Schmidt", # Ensure the method is compatible with the sensor
            red_weight="0.39",       # Optional: specify weighting factor for red channel
            green_weight="0.23",     # Optional: specify weighting factor for green channel
            blue_weight="0.21",      # Optional: specify weighting factor for blue channel
            infrared_weight="0.17",  # Optional: specify weighting factor for infrared channel
            sensor="WorldView-2" # Ensure the sensor type is correctly supported
        )
        # print("Pansharpened dataset created successfully.")
        return True
    except Exception as e:
        print(f"Failed to create pansharpened dataset: {str(e)}")
        return False


def convert_to_8bit(input_path, output_path, stretch_type="MinMax"):

    arcpy.CheckOutExtension("Spatial")
    inRaster = Raster(input_path)
    if stretch_type == "PercentClip":
        min_percent = 2
        max_percent = 98
        outRaster = arcpy.sa.Stretch(inRaster, StretchType="PercentClip", MinPercent=min_percent, MaxPercent=max_percent)
    elif stretch_type == "MinMax":
        # Determine good min/max values based on the image
        min_value = 0
        max_value = 16000  # Example max value for 16-bit images
        outRaster = arcpy.sa.RescaleByFunction(inRaster, arcpy.sa.RescalingFunctionMinMax(min_value, max_value))
    outRaster.save(output_path)
    arcpy.CheckInExtension("Spatial")


if __name__=="__main__":
    # print(arcpy.__version__)
    input_ms_path = r'c:\Users\ChiragPrabhakarPadub\Documents\PS\Engomi\ms'
    input_pan_path = r'c:\Users\ChiragPrabhakarPadub\Documents\PS\Engomi\pn'
    outputpath = r'c:\Users\ChiragPrabhakarPadub\Documents\PS\Engomi\ps'

    image_list = [file for file in os.listdir(input_ms_path) if file.endswith('.TIF')]

    for image in image_list:
        start_time = datetime.now()
        inpathms = os.path.join(input_ms_path,image)
        inpathpn = os.path.join(input_pan_path,image.replace('M','P'))
        outpath = os.path.join(outputpath, image)
        # print(os.path.exists(inpathms))
        # print(os.path.exists(inpathpn))
        # print(outpath)
        status = pansharpen(inpathms, inpathpn, outpath)

        if status:
            print("Pansharpened dataset created successfully. ")
        else:
            print(f"{image} Pansharpened Failled !!!!!")

        end_time = datetime.now()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time}")
        print("#######################################################################")

    # in_path = r'c:\Users\ChiragPrabhakarPadub\Documents\nicosia-pansharpenning\savvas-tasking-esa-data\050209502010_01\NIC-PS2\24APR01083706-M2AS_R1C5-050209502010_01_P002.TIF'
    # out_path = r'c:\Users\ChiragPrabhakarPadub\Documents\nicosia-pansharpenning\savvas-tasking-esa-data\050209502010_01\NIC-PS2-Render\24APR01083706-M2AS_R1C5-050209502010_01_P002.TIF'
    # convert_to_8bit(in_path,out_path)