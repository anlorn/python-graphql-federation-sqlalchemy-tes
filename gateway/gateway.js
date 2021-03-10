const { ApolloServer } = require("apollo-server");
const { ApolloGateway, RemoteGraphQLDataSource } = require("@apollo/gateway");
const fetch = require("node-fetch");

const AUDIT_URL = "http://localhost:4005/graphql";

function cleanIt(obj) {
	var cleaned = JSON.stringify(obj, null, 2);

	return cleaned.replace(/^[\t ]*"[^:\n\r]+(?<!\\)":/gm, function (match) {
		return match.replace(/"/g, "");
	});
}

const gateway = new ApolloGateway({
	// This entire `serviceList` is optional when running in managed federation
	// mode, using Apollo Graph Manager as the source of truth.  In production,
	// using a single source of truth to compose a schema is recommended and
	// prevents composition failures at runtime using schema validation using
	// real usage-based metrics.
	serviceList: [
		{ name: "legacy", url: "http://localhost:4006/graphql" },
		{ name: "stores", url: "http://0.0.0.0:5000/graphql" },
		{ name: "audit", url: AUDIT_URL },
		{ name: "providers", url: "http://0.0.0.0:4007/graphql" },
	],

	// Experimental: Enabling this enables the query plan view in Playground.
	__exposeQueryPlanExperimental: false,

	buildService({ url }) {
		return new RemoteGraphQLDataSource({
			url,
			willSendRequest({ request, context }) {
				//console.log({ request, context });
				request.http.headers.set(
					"user",
					context.user ? JSON.stringify(context.user) : null
				);
			},

			didReceiveResponse({ response, request, context }) {
				console.log("->", { response, request, context }, "<-");

				if (
					request.http.url !== AUDIT_URL &&
					request.query.startsWith("mutation")
				) {
					console.log("not audit url, starts with mutation");

					const requestToStore = `{query: ${cleanIt(
						request.query
					)}, variables: ${cleanIt(request.variables)} }`;

					const responseToStore = `{ data: ${cleanIt(
						response.data ? response.data : {}
					)}, errors: ${cleanIt(response.errors ? response.errors : {})} }`;

					console.log({ responseToStore });
					fetch(AUDIT_URL, {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							Accept: "application/json",
						},
						body: JSON.stringify({
							query: `mutation { insertNewChange(changeItem: { request: ${requestToStore}, response: ${responseToStore} })}`,
						}),
					})
						.then((r) => r.json())
						.then((data) => console.log("data returned:", data));
				}

				const cookie = request.http.headers.get("Cookie");
				if (cookie) {
					context.responseCookies.push(cookie);
				}

				// Return the response, even when unchanged.
				return response;
			},
		});
	},
});

(async () => {
	const server = new ApolloServer({
		gateway,

		// Apollo Graph Manager (previously known as Apollo Engine)
		// When enabled and an `ENGINE_API_KEY` is set in the environment,
		// provides metrics, schema management and trace reporting.
		engine: false,

		// Subscriptions are unsupported but planned for a future Gateway version.
		subscriptions: false,
	});

	server.listen({host: 'localhost', port: 6042}).then(({ url }) => {
		console.log(`🚀 Server ready at ${url}`);
	});
})();
