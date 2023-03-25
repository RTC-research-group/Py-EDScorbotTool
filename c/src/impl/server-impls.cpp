#include <string>
#include "../include/server-defs.hpp"

bool has_signal(std::string message){
    bool result = false;
	json json_obj = json::parse(message);

    result = json_obj.contains("signal");
	
	return result;
}

int extract_signal(std::string message){
    int result = 0;
	json json_obj = json::parse(message);

    result = json_obj["signal"];
	
	return result;
}

MetaInfoObject initial_metainfoobj(){
    MetaInfoObject result = MetaInfoObject();
    result.joints = std::list<JointInfo>(METAINFOS);

    return result;
}
