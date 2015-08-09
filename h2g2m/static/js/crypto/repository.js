H2G2M_cryptoModuleRepository = {

    _cryptoModules: [],

    hasMethods: function(obj /*, method list as strings */){
        var i = 1, methodName;
        while((methodName = arguments[i++])){
            if(typeof obj[methodName] != 'function') {
                return false;
            }
        }
        return true;
    },

    findAll: function() {
        return H2G2M_cryptoModuleRepository._cryptoModules;
    },

    findByName: function (name) {
        return H2G2M_cryptoModuleRepository._cryptoModules[name]
    },

    add: function (name, cryptoModule) {
        if (typeof(cryptoModule) !== 'object') {
            return false;
        }

        if (name in cryptoModule) {
            return false;
        }

        if (! H2G2M_cryptoModuleRepository.hasMethods(cryptoModule, "encrypt", "decrypt", "hash", "checkHash")) {
            return false;
        }

        H2G2M_cryptoModuleRepository._cryptoModules[name] = cryptoModule;

        return true;
    }
}
