MATCH (p:Project {ProjectId: "PRJ001"})
MATCH (b:Build {BuildId: "BUILD001"})
CREATE (p)-[:HAS_BUILD]->(b);

MATCH (b:Build {BuildId: "BUILD001"})
MATCH (s:AMSystem {AmSystemId: "SYS001"})
CREATE (b)-[:USED_SYSTEM]->(s);

MATCH (b:Build {BuildId: "BUILD001"})
MATCH (m:Material {MaterialId: "MAT001"})
CREATE (b)-[:USES_MATERIAL]->(m);

MATCH (m:Material {MaterialId: "MAT001"})
MATCH (f:Feedstock {FeedstockId: "FEED001"})
CREATE (m)-[:HAS_FEEDSTOCK]->(f);

MATCH (b:Build {BuildId: "BUILD001"})
MATCH (p:BuiltPart {BuiltPartId: "PART001"})
CREATE (b)-[:PRODUCED]->(p);

MATCH (p:BuiltPart {BuiltPartId: "PART001"})
MATCH (d:PartDesign {PartDesignId: "PD001"})
CREATE (p)-[:INSTANCE_OF]->(d);

MATCH (b:Build {BuildId: "BUILD001"})
MATCH (p:ProcessControl {ProcessId: "PROC001"})
CREATE (b)-[:USED_PROCESS]->(p);

MATCH (b:Build {BuildId: "BUILD001"})
MATCH (m:InSituMonitoringSystem {InSituSystemId: "MON001"})
CREATE (b)-[:MONITORED_BY]->(m);

MATCH (p:BuiltPart {BuiltPartId: "PART001"})
MATCH (t:TIC {TicId: "TIC001"})
CREATE (p)-[:UNDERWENT_TIC]->(t);

MATCH (t:TIC {TicId: "TIC001"})
MATCH (r:TestResult {ResultId: "TR001"})
CREATE (t)-[:GENERATED_RESULT]->(r);

