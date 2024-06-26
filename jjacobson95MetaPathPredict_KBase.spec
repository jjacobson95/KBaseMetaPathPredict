/*
A KBase module: jjacobson95MetaPathPredict_KBase
*/

module jjacobson95MetaPathPredict_KBase {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_jjacobson95MetaPathPredict_KBase(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
