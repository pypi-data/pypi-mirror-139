# Python Mercure (pymcure) [Français]

L'objectif de cette bibliothèque est de fournir un moyen rapide de publier et de consommer des messages sur Mercure. 
Si vous ne savez pas ce qu'est Mercure, jetez un coup d'œil ici: (https://github.com/dunglas/mercure).

Cette bibliothèque est actuellement en cours de développement, 
donc si vous trouvez un bogue ou une chance d'amélioration, veuillez nous en faire part. :)

Nous nous sommes inspirés de la bibliotheque pymercure créée et maintenue par Vitor Villar (Salut Vitor :) ) qui est consultable ici https://github.com/vitorluis/python-mercure

## Installation de la bibliothèque

La bibliothèque est disponible sur PyPi, vous pouvez donc l'installer en utilisant pip :

     pip3 install pymcure

## Publication des messages

Comme mentionné précédemment, l'objectif est de fournir un moyen rapide de publier des messages.
Et pour ce faire, il a fourni les classes Sync et Async.
 
 
### Publication des messages Synchrone

```python
import json
from pymcure.client.publisher.sync import SyncPublisher
from pymcure.client.message import Message

data = json.dumps({'status': 'test'})
msg = Message(['mytopicname'], data)
publisher = SyncPublisher(mercure_hub='http://127.0.0.1:3000/.well-known/mercure',mercure_jwt=None,secret='your.secret.phrase'
)
publisher.publish(msg)
```
#### La classe SyncPublisher a pour paramettre
##### mercure_hub 
Le lien du hub mercure 

##### mercure_jwt
Le token JWT pour s'authentifier sur le hub. Si vous ne voulez pas generer vous même votre token donner la valeur ```None```
et definissez les paramettres suivant

##### secret
Je mot secret utilisé pour demarrer le hub

#### payload
Le payload est defini par defaut, mais vous pouvez definir le votre

definition par defaut
```json
PAYLOAD = {
    "mercure": {
        "subscribe": [
        ],
        "publish": [
        ]
    }
}
```

#### header
Le header est definir par defaut, mais vous pouvez definir le votre

definition par defaut
```json
HEADER = {
    "typ": "JWT",
    "alg": "HS256"
}
```

### Publication des messages Asynchrone

```python
import json
from pymcure.client.publisher.asynch import AsyncPublisher
from pymcure.client.message import Message

data = json.dumps({'status': 'test'})
msg = Message(['mytopicname'], data)
publisher = AsyncPublisher(
     'http://127.0.0.1:3000/.well-known/mercure',
     'your.Token.Here'
)
publisher.publish(msg)
```

Dans le cas d'une asynchronisation, la demande sera faite en utilisant la bibliothèque de gevent.

## Consommation de messages

Pour consommer des messages, c'est aussi assez simple. car le consommateur court dans un nouveau fil
vous n'avez pas à vous en préoccuper, il vous suffit de lui passer une fonction de rappel:

```python
from pymcure.client.consumer import Consumer

def callback(message):
    print(message.data)


c = Consumer('http://127.0.0.1:3000/.well-known/mercure', ['mytopicname'], callback)
c.start_consumption()
```

Lors de votre rappel, vous recevrez toujours l'objet "Message", avec les données et les métadonnées du message.

## BONUS
Pour demarrer le hub mercure il faut soit:

### Docker

Mode demo
```shell
docker run -e JWT_KEY='!ChangeMe!' -e DEMO=1 -e ALLOW_ANONYMOUS=1 -e CORS_ALLOWED_ORIGINS=* -e PUBLISH_ALLOWED_ORIGINS='*' -p 80:80 dunglas/mercure
```

Mode prod
```shell
docker run \
    -e JWT_KEY='!ChangeMe!' -e ACME_HOSTS='*' \
    -p 80:80 -p 443:443 \
    dunglas/mercure
```

### Binaire
Téléchargez le binaire qui convient à votre système ici https://github.com/dunglas/mercure/releases
Se déplacer dans le repertoire et executer le binaire avec les paramettre suivant

```shell
JWT_KEY='your.secrer.phrase' ADDR=:3000 DEMO=1 ALLOW_ANONYMOUS=1 PUBLISH_ALLOWED_ORIGINS='*' CORS_ALLOWED_ORIGINS='*' ./mercure
```

## Crédits

Créé et maintenu par Vianney ADOU <adoujmv@gmail.com>


# Python Mercure (pymcure) [English]