# Automatic Endpoint Generation

Run the bash script: `bash create_backend_openapi_template.sh`  
This will:
- Generate the openapi specification of the backend fastapi app
- Autogenerate a typescript template based on the generated openapi specification with the `openapitools/openapi-generator-cli` module

# Usage

The generated template can be used to access the

- Routes
- Parameter Schemas
- Response Schemas
- Types

of the backend app.  

Usage example:
``` ts
import {Configuration, UserApi, type UserSchema} from '@generated-sources'

function useConfiguration(){
    return new Configuration({basePath: window.location.origin});
}

function useUserApi(){
    return new UserApi(useConfiguration());
}

var user: Ref<UserSchema> = ref();

async function getUser(){
    user.value = await useUserApi().getUsers({name: 'Skywalker', surname: 'Luke'});
}

```