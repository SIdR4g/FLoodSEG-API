# FloodSEG API

## Overview
The Floodseg API is a powerful tool designed for precise flood monitoring using advanced image segmentation techniques. Leveraging technologies such as PyTorch, OpenCV, and the DeepLabV3 model, this API provides accurate segmentation of flood-affected areas from input images. Additionally, it offers user registration, login functionalities, and secure authentication through JSON Web Tokens (JWT). An innovative feature allows users to submit fragmented images of the same flood-prone region, and the API intelligently stitches these segments post-segmentation, providing high-resolution, comprehensive visuals for enhanced flood monitoring.

## Features
1. **Image Segmentation:**
   - Utilizes PyTorch and DeepLabV3 for accurate segmentation of flood-affected areas from input images.
   - Employs OpenCV for post-processing, ensuring precise and detailed results.

2. **User Authentication:**
   - Seamless registration and login functionalities for user access.
   - JSON Web Tokens (JWT) ensure secure and confidential authentication.

3. **High-Resolution Image Stitching:**
   - Unique feature allows users to submit fragmented images of the same flood-prone region.
   - API intelligently stitches these segments post-segmentation, delivering high-resolution, comprehensive visuals.

## Getting Started

### Prerequisites
- Python 3.x
- Django
- DjangoRestFramework
- PyTorch
- OpenCV
- Roboflow
  
### Linux Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/SIdR4g/FLoodSEG-API.git
   cd floodapi
   ```
   
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

### API Endpoints

- **Endpoint 1:** `/home/account/register`
  - Method: POST
  - Description: Register a new user.
  - Request Body: 

      ![Screenshot 2023-12-23 161733](https://github.com/SIdR4g/FLoodSEG-API/assets/78850085/e75e9b65-0356-4551-9dbf-0c3b39e035b3)


- **Endpoint 2:** `/home/account/login`
  - Method: POST
  - Description: Log in and obtain authentication token.
  - Request Body: 
  
      ![Screenshot 2023-12-23 161834](https://github.com/SIdR4g/FLoodSEG-API/assets/78850085/d06dadb7-d822-4fdf-91e2-c15595150aea)

-  **Endpoint 3:** `/home/api/upload/`
  - Method: POST
  - Description: Perform flood area segmentation on input images.
  - Request Body:
    
    ![Screenshot 2023-12-23 161207](https://github.com/SIdR4g/FLoodSEG-API/assets/78850085/fc33806f-90ba-42b1-a3ad-396e5c0c8145)

- **Endpoint 4:** `/home/api/upload/`
  - Method: GET
  - Description: Gets all the data relating to the previous uploaded images from the database.

- **Endpoint 5:** `/home/api/upload_patch/`
  - Method: POST
  - Description: Perform flood area segmentation on input images.
  - Request Body:
    ![Screenshot 2023-12-23 161413](https://github.com/SIdR4g/FLoodSEG-API/assets/78850085/a58fdb40-d001-468b-b22c-0ed5cb4feb23)

- **Endpoint 6:** `/api/home/upload_patch?search=<patch_code>&merge=<"segment">&patch_dimension=<>`
  - Method: GET
  - Description: Searches all the images having the same patch code and merges the segmented images by the dimension given .For example:- 2X2 means there are 4 images and order them by their id in 2X2 format
  

## License
This project is licensed under the [MIT License](LICENSE).


Feel free to explore the codebase and contribute to the development of this innovative flood monitoring solution!
