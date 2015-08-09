(function ($, cryptoModuleRepository, passwordStorage) {
    function getFormLine($form, type, id, label, entries) {
        var uiElement;

        if (type === 'select') {
            uiElement = getFormSelect(id, entries);
        } else {
            uiElement = getFormInput(type, id);
        }
        return $('<div class="form-group"><label for="' + id + '">' + label + '</label>' + uiElement + '</div>');
    }

    function getFormInput(type, id) {
        return '<input id="' + id + '" name="' + id + '" type="' + type + '">';
    }

    function getFormSelect(id, entries) {
        if (!entries) return '';
        var ret = '<select name="' + id + '" id="' + id + '">';

        entries.forEach(function (entry) {
            ret += '<option value="' + entry + '">' + entry + '</option>';
        });

        ret += '</select>';

        return ret;
    }

    function enhanceForm(id) {
        var $form = $('#' + id);
        var $fieldset = $form.find('fieldset');

        var $encrypt = getFormLine($form, 'checkbox', 'encrypt', 'Encrypt');
        var $cryptoModule = getFormLine($form, 'select', 'crypto-module', 'Crypto-Module', Object.keys(cryptoModuleRepository.findAll()));
        var $cryptoPassword = getFormLine($form, 'select', 'crypto-password', 'Password', passwordStorage.keys());
        var $cryptoPasswordAddButton = $('<a href="#"><span class="glyphicon glyphicon-plus"></span></a>')

        $cryptoPasswordAddButton.click(askForPassword);

        var $encryptCheckbox = $($encrypt.find('input[type=checkbox]')[0]);
        $fieldset.append($encrypt);
        var encryptCheckboxChange = function () {
            if ($encryptCheckbox.is(':checked')) {
                $cryptoModule.show();
                $cryptoPassword.show();
                $cryptoPasswordAddButton.show();
            }
            else {
                $cryptoModule.hide();
                $cryptoPassword.hide();
                $cryptoPasswordAddButton.hide();
            }
        };
        encryptCheckboxChange();
        $encryptCheckbox.change(encryptCheckboxChange);

        $fieldset.append($cryptoModule);
        $fieldset.append($cryptoPassword);
        $fieldset.append($cryptoPasswordAddButton);
    }

    var $keyMenu = $('<ul class="dropdown-menu"></ul>');

    function removePassword() {
        var name = $(this).find('a').text().trim();
        if (confirm('Do you want to remove the password with the name "' + name + '"')) {
            passwordStorage.remove(name);
            $('select[name="crypto-password"] option[value="' + name + '"').remove();
            $(this).remove();
        }
    }

    function askForPassword() {
        var name = prompt('Please enter a unique name for the password (it is saved to local password storage with that name):');
        if (name === null) {
            return;
        }
        if (passwordStorage.isSet(name)) {
            alert('A password with this name already exists, choose a different name!')
            return;
        }
        var password = prompt('Please enter password:');
        if (password === null) {
            return;
        }
        $('select[name="crypto-password"]').append($('<option value="' + name + '">' + name + '</option>'));
        passwordStorage.set(name, password);
        addPasswordToMenu(name);
    }

    function addPasswordToMenu(name) {
        var $newEntry = $('<li><a href="#"><span class="glyphicon glyphicon-trash"></span> ' + name + '</a></li>');
        $keyMenu.prepend($newEntry);
        $newEntry.click(removePassword);
    }

    function enhanceMenu() {
        var $keyMenuButton = $('<li class="dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown">Keys <b class="caret"></b></a></li>')
        var $addButton = $('<li role="separator" class="divider"></li><li><a href="#"><span class="glyphicon glyphicon-plus"></span> Add</a></li>');
        $addButton.click(askForPassword);
        $keyMenu.append($addButton);
        passwordStorage.keys().forEach(function (elem) {
            addPasswordToMenu(elem, passwordStorage.get(elem));
        });
        $keyMenuButton.append($keyMenu);
        $('.navbar-right').append($keyMenuButton);
    }

    $(document).ready(function () {
        enhanceForm('TxtForm');
        enhanceMenu();

        //$encryptBtn.click(function () {
        //    var password = askForPassword();
        //    $('input[type=text],textarea').each(function (i, input) {
        //        $(input).val(encrypt($(input).val(), password));
        //    });
        //});
        //$decryptBtn.click(function () {
        //    var password = askForPassword();
        //    $('input[type=text],textarea').each(function (i, input) {
        //        $(input).val(decrypt($(input).val(), password));
        //    });
        //    $('span').each(function (i, div) {
        //        var $div = $(div);
        //        var cipherText = $div.text();
        //        var decrypted = decrypt(cipherText, password);
        //        if (encrypt(decrypted, password) == cipherText) {
        //            $div.text(decrypted);
        //        }
        //    })
        //});
    });
})(jQuery, H2G2M_cryptoModuleRepository, $.initNamespaceStorage('cryptoPasswords').localStorage);
