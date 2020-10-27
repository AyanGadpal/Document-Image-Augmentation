import os
import argparse
import cv2
from DocumentAugmentation import DocumentAugmentation
import glob 

def SingleImage(src,des):
  image = cv2.imread(src)

  # Perform Augmentation
  Dialated = DocumentAugmentation.Dialate(image) # Do not use for OCR
  Smudged = DocumentAugmentation.Smudge(image) # Do not use for OCR 
  colored = DocumentAugmentation.changeColor(image) # This will randomly select color
  BUimage = DocumentAugmentation.BrightnessUp(image)
  BDimage = DocumentAugmentation.BrightnessDown(image)
  
  # file name
  s = src.split("/")[-1].split(".")[:-1]
  filename = ' '.join([str(elem) for elem in s])

  print("Processing : ",filename)
  # Save Augmentations (.jpg and .png Only)
  if des is None:
    des = src
  else:
    des += filename

  print("Saving to ",des)
  cv2.imwrite(des+"_dialation.jpg",Dialated)
  cv2.imwrite(des+"_Smudged.jpg",Smudged)
  cv2.imwrite(des+"_colored.jpg",colored)
  cv2.imwrite(des+"_BUimage.jpg",BUimage)
  cv2.imwrite(des+"_BDimage.jpg",BDimage)

def MultipleImage(src,des):
  images = glob.glob(src)
  for image in images:
    SingleImage(image,des)

def parse_args():
  parser = argparse.ArgumentParser(description="WB color augmenter")
  p = parser.add_argument
  p("--input_image_filename", help="Input image's full filename (for a single image augmentation)")
  p("--input_image_dir", help="Training image directory (use it for batch processing)")
  p("--out_dir", help="Output directory")
  p("--write_original", type=int, default=1, help="Save copy of original image(s) in out_dir")
  return parser.parse_args()

def main():
  args = parse_args()
  if args.input_image_filename is not None:
    if args.out_dir is None:
          args.out_dir = "./Augmented/"
    os.makedirs(args.out_dir, exist_ok=True)  # create output training directory (if not exist)
    SingleImage(args.input_image_filename,args.out_dir)
  elif input_image_dir is not None:
    if args.out_dir is None:
        args.out_dir = "./Augmented/"
    os.makedirs(args.out_dir, exist_ok=True) 
    MultipleImage(args.input_image_dir,args.out_dir)

if __name__ == "__main__":
    main()
