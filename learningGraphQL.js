const {ApolloServer} = require('apollo-server');
const { promisify } = require('util');
const exec = promisify(require('child_process').exec)
const { gql } = require('apollo-server');

const typeDefs = gql`
# Query/Mutations/ must have a matching resolvers
type SystemData {    
 username: String!
 loadAverage: String!
 diskUtil: String!
     }

type Query {
    querySystemData: SystemData!
}

`
async function getSystemData() {
    async function getSystemData() {
        const user = await exec("w |  awk '{print $1}' | sort -u | grep -v USER | grep -v ':'")
        const loadAverage = await exec('uptime | awk \'{print $10 " " $11 " " $12  }\'')
        const diskUtil =  await exec("df -h | grep 'xvda' | awk  '{print $5}' | head -n 1")
         return { username:user.stdout.trim(),
                loadAverage:loadAverage.stdout.trim(),
               diskUtil: diskUtil.stdout.trim()}
    
        }

const resolvers = {
    Query:{   querySystemData:getSystemData   }   }
            

const apolloServer = new ApolloServer({
    typeDefs,
    resolvers
   
});

apolloServer.listen({ port: 5000}).then((res) => {
    console.log(`Server running at ${res.url}`)
});


// AWS EC2 GraphQL practice - Queries and Resolvers 
// Running Apollo Server from EC2 - using basic query and resolver to fetch basic system data 
// Elliott Arnold  12-13-20
