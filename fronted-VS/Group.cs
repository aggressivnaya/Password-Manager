using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace password_manager
{
    public class Group
    {
        public string GroupName { get; set; }
        public List<string> Members { get; set; }
        public List<Password> GroupPasswords { get; set; }
    }
}
