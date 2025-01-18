import os
import sys
sys.path.append(os.getcwd())

from db.repository.images_store_repository import del_image_from_db


del_image_from_db('e88e494abed3488db2e4532188eb3adb')
