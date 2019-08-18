### API for application helpdesk ticket

### Production domain : https://
### Test domain : https://
## List api for application
# Hanoi 18/08/2019



## 1. API Login [/api/v1/users/login]

### Login Method [POST]

+ Request
   + Headers

            Content-Type: application/json

   + Body

            {
                "login": "phongng@gmail.com",
                "password":"12345"
            }

   + Schema

            {
                "type": "object",
                "required": ["login","password"],
                "properties": {
                    "email": {"type": "string" },
                    "password": {"type": "string" }

                }
            }

+ Response 200 (application/json)
    + Body

            {
                "name": "Nguyễn Gia Phong",
                "token": "f9bcbe08106b497a8d81d6ed35aee639",
            }
    + Schema

            {
                "type": "object",
                "required": ["name","token"],
                "properties": {
                    "name": {"type": "string" },
                    "token": {"type": "string" }

                }
            }


## 2. API get list tickets for user  [/api/v1/tickets]
### [GET]
+ Request
    + Headers
            Content-Type: application/json
            Authorization : token
            
+ Response 200 (application/json)
    + Body
        
            {
                "id_ticket" : 1,
                "name_ticket": "TK0123",
                "description": "Thu tiền nước",
                "partner_address": "Số 7, Lý thường kiệt",
                "partner_ref": "21007235",
                "image_url": "http://gssds.sdfs/avatar.png",
                "expired_to_text": "Finish"
            }
    + Schema

            {
                "type": "object",
                "required": ["id_ticket","name_ticket"],
                "properties": {
                    "id_ticket": {"type": "integer" },
                    "name_ticket": {"type": "string" },
                    "description": {"type": "string" },
                    "partner_address": {"type": "string" },
                    "partner_ref":{"type":"string"},
                    "image_url": {"type": "string"},
                    "expired_to_text": {"type": string}

                }
            }



## 3. API get more info  for ticket  [/api/v1/tickets/{id_ticket}]
### [GET]
+ Request
    + Headers
            Content-Type: application/json
            Authorization : token

+ Response 200 (application/json)
    + Body

            {
                "partner_phone": "037XXXXXXXX",
                "create_name": "Nguyễn Văn XXX",
                "image_url": ["http://gssds.sdfs/avatar.png"],
                "assigin_date": "01/01/2019"
            }
    + Schema

            {
                "type": "object",
                "properties": {
                    "partner_phone": {"type": "string" },
                    "create_name":{"type":"string"},
                    "image_url": {"type": "array"},
                    "assigin_date": {"type": Date}

                }
            }


### 4.Update ticket [PUT]
## Kêt quả hoàn thành tickets [/api/v1/tickets/update/{id_ticket}]
### [PUT]
+ Request
    + Headers

            Content-Type: application/json
            Authorization : token
    + Body
            {
                "image_url": [http://gssds.sdfs/avatar.png",],
                "results": "Đã thu tiền nước",
                "lat": 112.04 ,
                "lng": 3234.0
            }

    + Schema

            {
                "type": "object",
                "required": ["result"],
                "properties": {
                    "image_url": {"type": "array" },
                    "results":{"type":"string"},
                    "lat": {"type": "float"},
                    "lng": {"type": "float"}

                }
            }
        
+ Response 200 (application/json)
    + Body
    
            {
                "result":"success",
            }
    + Schema

            {
                "type": "object",
                "properties": {
                    "result":{"type":"string"},
                }
            }

### 5. Update problem ticket [PUT]
## Báo cáo sự cố  tickets [/api/v1/tickets/problem/{id_ticket}]
### [PUT]
+ Request
    + Headers

            Content-Type: application/json
            Authorization : token
    + Body
            {
                "image_url": [http://gssds.sdfs/avatar.png",],
                "work_incident": "Bị vỡ ống nước",
                "lat": 112.04 ,
                "lng": 3234.0
            }

    + Schema

            {
                "type": "object",
                "required": ["work_incident", "image_url"],
                "properties": {
                    "image_url": {"type": "array" },
                    "work_incident":{"type":"string"},
                    "lat": {"type": "float"},
                    "lng": {"type": "float"}
                }
            }

+ Response 200 (application/json)
    + Body

            {
                "result":"success",
            }
    + Schema

            {
                "type": "object",
                "properties": {
                    "result":{"type":"string"},
                }
            }


###Bảng mã lỗi
+ 200 - success. Thực hiện giao dịch thành công 
+ 400 - Bad request. Các tham số đầu vào không hợp lệ
+ 401 - Authorization required. Token không hợp lệ
+ 403 - Not allowed. Phương thức không hợp lệ
+ 404 - Not found. Không tìm thấy thông tin yêu cầu
+ 408 - Timeout. Giao dịch bị timeout
+ 500 - Internal error. Lỗi hệ thống, liên hệ với quản trị viên
+ 503 - Hệ thống đang bảo trì
