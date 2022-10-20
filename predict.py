import os, time, uuid
import argparse
import asyncio

import functions

def predict(path):
    byte_imgs = functions.images2bytes(path)
    # print(byte_imgs)
    loop = asyncio.get_event_loop()
    rsps = loop.run_until_complete(functions.fetch_all(byte_imgs))

    print(rsps)

def parse_args():
    parser = argparse.ArgumentParser(description='Prediction args')
    parser.add_argument('--data_path', type=str, help='Prediction image folder', 
                        default=r"D:\_Innospire\data\vehicle_recognition_test")
    parser.add_argument('--save_path', type=str, help='Path to save predicted images', 
                        default=r"")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    predict(args.data_path)