using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace password_manager
{
    public class Password
    {
        public string Website { get; set; }
        public string Username { get; set; }
        public string PasswordText { get; set; }

        // Property to display masked password
        public string PasswordMasked => new string('*', PasswordText.Length);
    }
}
