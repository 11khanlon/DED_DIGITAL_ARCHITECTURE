CREATE (:Project {
    ProjectId: "PRJ001",
    ProjectName: "DED Tracebility"
});

CREATE (:Build {
    BuildId: "BUILD001",
    BuildStatus: "COMPLETE",
    StartTime: "2026-05-01T08:00:00",
    EndTime: "2026-05-01T15:00:00",
    LayerCount: 4200
});

CREATE (:Material {
    MaterialId: "MAT001",
    MaterialName: "IN625",
    MaterialGrade: "ASTM F3056"
});

CREATE (:Feedstock {
    FeedstockId: "FEED001",
    IngotId: "INGOT77"
});

CREATE (:Substrate {
    SubstrateId: "SUB001"
});

CREATE (:BuiltPart {
    BuiltPartId: "PART001",
    Orientation: "VERTICAL"
});

CREATE (:PartDesign {
    PartDesignId: "PD001"
});

CREATE (:ProcessControl {
    ProcessId: "PROC001",
    LayerThicknessUm: 40,
    ChamberOxygenLimitPpm: 100
});

CREATE (:TIC {
    TicId: "TIC001",
    TicType: "CT_SCAN",
    PassFail: "PASS"
});

CREATE (:TestResult {
    ResultId: "TR001",
    MeasurementType: "POROSITY",
    Value: 0.03,
    Unit: "percent"
});


Build
Part
Machine
Layer
ScanTrack
ParameterSet
PowderBatch
Operator
ThermalRegion
Defect
SensorMeasurement
Toolpath
GeometryRegion
PostProcessOperation

(Build)-[:USES_MATERIAL]->(PowderBatch)

(Part)-[:BUILT_IN]->(Build)

(Layer)-[:CONTAINS]->(ScanTrack)

(ScanTrack)-[:USES_PARAMETERS]->(ParameterSet)

(Defect)-[:OBSERVED_IN]->(Layer)