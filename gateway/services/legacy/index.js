const { ApolloServer, gql } = require("apollo-server");
const { buildFederatedSchema } = require("@apollo/federation");
const GraphQLJSON = require("graphql-type-json");
const fetch = require("node-fetch");

const allChanges = [];
const CONSUL_URL = "http://127.0.0.1:8500/";

const typeDefs = gql`
	scalar JSON

	input configInput {
		tenant: String
		key: String
		value: JSON
	}

	extend type Mutation {
		setConfig(configInput: configInput): Boolean
	}

	extend type Query {
		getConfig(tenant: String, key: String): JSON
	}
`;

const resolvers = {
	Query: {
		async getConfig(_, { tenant, key }) {
			const response = await fetch(
				`${CONSUL_URL}/v1/kv/${tenant}/${key}?raw=true`
			);

			return await response.json();
		},
	},
	Mutation: {
		async setConfig(_, { configInput }) {
			console.log({ configInput }, JSON.stringify(configInput["value"]));

			const read = await fetch(
				`${CONSUL_URL}/v1/kv/${configInput["tenant"]}/${configInput["key"]}`,
				{
					body: JSON.stringify(configInput["value"]),

					headers: {
						"Content-Type": "application/x-www-form-urlencoded",
					},
					method: "PUT",
				}
			);

			//onsole.log(read.json());

			allChanges.push({ ...configInput, timestamp: new Date() });
			return true;
		},
	},
};

const server = new ApolloServer({
	schema: buildFederatedSchema([
		{
			typeDefs,
			resolvers,
		},
	]),
});

server.listen({ port: 4006, host: '127.0.0.1' }).then(({ url }) => {
	console.log(`🚀 Server ready at ${url}`);
});

const inventory = [
	{ upc: "1", inStock: true },
	{ upc: "2", inStock: false },
	{ upc: "3", inStock: true },
URLSearchParams];
