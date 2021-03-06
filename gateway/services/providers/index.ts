
import { delegateToSchema, makeExecutableSchema } from 'graphql-tools';
import { ApolloServer } from 'apollo-server';
import { transformSchemaFederation } from 'graphql-transform-federation';
import createSchema, { CallBackendArguments } from 'swagger-to-graphql';
import fetch from 'node-fetch';
import { URLSearchParams } from 'url';


function getBodyAndHeaders(
  body: any,
  bodyType: 'json' | 'formData',
  headers: { [key: string]: string } | undefined,
) {
  if (!body) {
    return { headers };
  }

  if (bodyType === 'json') {
    return {
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      body: JSON.stringify(body),
    };
  }

  return {
    headers,
    body: new URLSearchParams(body),
  };
}

async function callBackend({
  requestOptions: { method, body, baseUrl, path, query, headers, bodyType },
}: CallBackendArguments<{}>) {
  const searchPath = query ? `?${new URLSearchParams(query)}` : '';
  const url = `http://localhost:8080/${baseUrl}${path}${searchPath}`;
  const bodyAndHeaders = getBodyAndHeaders(body, bodyType, headers);

  console.log(`-------- ${url}`);
  const response = await fetch(url, {
    method,
    ...bodyAndHeaders,
  });

  const text = await response.text();
  if (response.ok) {
    try {
      return JSON.parse(text);
    } catch (e) {
      return text;
    }
  }
  throw new Error(`Response: ${response.status} - ${text}`);
}

(async function main() {
  const schemaWithoutFederation = await createSchema({
    swaggerSchema: 'http://localhost:8080/v1/openapi.json',
    callBackend,
  });

  const federationSchema = transformSchemaFederation(schemaWithoutFederation, {});

  const { url } = await new ApolloServer({
    schema: federationSchema,
  }).listen({
    port: 4007,
    host: '127.0.0.1'
  });

  console.log(`🚀 Swagger server ready at ${url}`);
})();
