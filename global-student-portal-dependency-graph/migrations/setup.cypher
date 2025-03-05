CREATE (:Component {name: 'AuthService'});
CREATE (:Component {name: 'UserService'});
CREATE (:Component {name: 'CourseService'});
CREATE (:Component {name: 'PaymentService'});
CREATE (:Component {name: 'NotificationService'});

MATCH (a:Component {name: 'AuthService'}), (b:Component {name: 'UserService'})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (b:Component {name: 'UserService'}), (c:Component {name: 'CourseService'})
CREATE (b)-[:DEPENDS_ON]->(c);

MATCH (c:Component {name: 'CourseService'}), (d:Component {name: 'PaymentService'})
CREATE (c)-[:DEPENDS_ON]->(d);

MATCH (d:Component {name: 'PaymentService'}), (e:Component {name: 'NotificationService'})
CREATE (d)-[:DEPENDS_ON]->(e);
