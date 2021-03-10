const { ApolloServer, gql } = require("apollo-server");
const { buildFederatedSchema } = require("@apollo/federation");
const GraphQLJSON = require("graphql-type-json");

const allChanges = [];

const typeDefs = gql`
	scalar JSON

	input ChangeItem {
		request: JSON
		response: JSON
	}

	extend type Mutation {
		insertNewChange(changeItem: ChangeItem): Boolean
	}

	extend type Query {
		getChanges: [JSON]
	}
`;

const resolvers = {
	Query: {
		getChanges() {
			return allChanges;
		},
	},
	Mutation: {
		insertNewChange(_, args) {
			console.log({ args });
			allChanges.push({ ...args, timestamp: new Date() });
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

server.listen({host: '127.0.0.1', port: 4005 }).then(({ url }) => {
	console.log(`🚀 Server ready at ${url}`);
});

const inventory = [
	{ upc: "1", inStock: true },
	{ upc: "2", inStock: false },
	{ upc: "3", inStock: true },
];
