const {
  Environment,
  Network,
  RecordSource,
  Store,
} = require('relay-runtime')

const source = new RecordSource()
const store = new Store(source)

function fetchQuery(
  operation,
  variables,
) {
  return fetch('/graphql', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Access-Control-Request-Method': 'POST',
      'Access-Control-Request-Headers': 'Content-Type, Access-Control-Allow-Headers',
    },
    credentials: 'same-origin',
    body: JSON.stringify({
      query: operation.text, // GraphQL text from input
      variables,
    }),
  }).then(response => {
    return response.json();
  });
}

const network = Network.create(fetchQuery);

const environment = new Environment({
  network,
  store,
});

export default environment
