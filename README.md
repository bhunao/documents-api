# TEMPLATE

## run tests
```shell
docker run -it --rm template_fastapi-web pytest
```


## database
- feed
    - news
        - news_review
- user
    - user_favorites
    - user_filter


### schema
#### feed
| name          | type      |
|-------------- | --------- |
| id            | int       |
| link          | str       |
| name          | str       |

#### news
| name          | type      |
|-------------- | --------- |
| id            | int       |
| feed_id       | str       |
| title         | str       |
| summary       | str       |
| link          | str       |
| published     | datetime  |
| media_content | str       |

#### news review
| name          | type      |
|-------------- | --------- |
| user_id       | int       |
| news_id       | str       |
| review        | str       |
| tags          | str       |

#### user
| name          | type      |
|-------------- | --------- |
| id            | int       |
| username      | str       |
| password      | str       |
| email         | str       |
| is_active     | bool      |
| created_at    | datetime  |


#### user filter
| name          | type      |
|-------------- | --------- |
| user_id       | int       |
| name          | int       |
| filter_type   | str       |
| filter        | str       |
| created_at    | datetime  |

#### user favorites
| name          | type      |
|-------------- | --------- |
| user_id       | int       |
| news_id       | int       |
| created_at    | datetime  |

## business logic
### agregador de noticias
### classificação de noticias
### classificação do usuario
### news across metrics (clicks and stuff)

## backend
### autenticação
### CRUD base
### rotas
### testes


## frontend
### list view
### card view
![01](images/card_01.jpeg) 
![02](images/card_02.jpeg) 
![03](images/card_03.jpeg) 
### single item

## host
?
