import React, { useState } from 'react';
import { 
  Users, 
  Building2, 
  Phone, 
  Mail, 
  Calendar, 
  DollarSign, 
  TrendingUp, 
  Search,
  Plus,
  Filter,
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  Lock,
  User,
  LogOut,
  AlertCircle
} from 'lucide-react';

const CRMApp = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [loginError, setLoginError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Demo credentials for testing
  const DEMO_CREDENTIALS = {
    email: 'admin@crm.com',
    password: 'password123'
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setLoginError('');

    // Simulate API call
    setTimeout(() => {
      if (loginForm.email === DEMO_CREDENTIALS.email && loginForm.password === DEMO_CREDENTIALS.password) {
        setIsAuthenticated(true);
        setLoginError('');
      } else {
        setLoginError('Invalid email or password. Try admin@crm.com / password123');
      }
      setIsLoading(false);
    }, 1000);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setLoginForm({ email: '', password: '' });
    setLoginError('');
  };

  const LoginPage = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-purple-800 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <div className="bg-blue-600 p-3 rounded-full">
              <Building2 className="w-8 h-8 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Nirvaha</h1>
          <p className="text-3xl font-bold text-gray-900 mb-2">Starry Financial Services</p>
          <p className="text-gray-600">Sign in to your account</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <div className="relative">
              <User className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="email"
                required
                value={loginForm.email}
                onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your email"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="password"
                required
                value={loginForm.password}
                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your password"
              />
            </div>
          </div>

          {loginError && (
            <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              <AlertCircle className="w-4 h-4" />
              {loginError}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Signing in...
              </div>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
            <p className="font-medium mb-1">Demo Credentials:</p>
            <p>Email: admin@crm.com</p>
            <p>Password: password123</p>
          </div>
        </div>

        <div className="mt-6 text-center text-sm text-gray-600">
          <a href="#" className="text-blue-600 hover:text-blue-700 font-medium">
            Forgot your password?
          </a>
        </div>
      </div>
    </div>
  );

  const CRMDashboard = () => {
    const [activeTab, setActiveTab] = useState('dashboard');
    const [searchTerm, setSearchTerm] = useState('');

    // Sample data
    const customers = [
      { id: 1, name: 'John Smith', company: 'Tech Corp', email: 'john@techcorp.com', phone: '+1-555-0123', status: 'Active', value: '$45,000' },
      { id: 2, name: 'Sarah Johnson', company: 'StartupXYZ', email: 'sarah@startupxyz.com', phone: '+1-555-0124', status: 'Lead', value: '$12,000' },
      { id: 3, name: 'Mike Brown', company: 'Enterprise Ltd', email: 'mike@enterprise.com', phone: '+1-555-0125', status: 'Active', value: '$78,000' },
      { id: 4, name: 'Lisa Davis', company: 'Innovation Hub', email: 'lisa@innovation.com', phone: '+1-555-0126', status: 'Inactive', value: '$23,000' }
    ];

    const deals = [
      { id: 1, title: 'Website Redesign', customer: 'Tech Corp', value: '$45,000', stage: 'Negotiation', probability: '80%' },
      { id: 2, title: 'Mobile App Development', customer: 'StartupXYZ', value: '$12,000', stage: 'Proposal', probability: '60%' },
      { id: 3, title: 'Cloud Migration', customer: 'Enterprise Ltd', value: '$78,000', stage: 'Closed Won', probability: '100%' },
      { id: 4, title: 'Marketing Campaign', customer: 'Innovation Hub', value: '$23,000', stage: 'Discovery', probability: '30%' }
    ];

    const stats = [
      { title: 'Total Customers', value: '1,234', change: '+12%', icon: Users, color: 'text-blue-600' },
      { title: 'Active Deals', value: '45', change: '+8%', icon: DollarSign, color: 'text-green-600' },
      { title: 'Revenue This Month', value: '$125,430', change: '+15%', icon: TrendingUp, color: 'text-purple-600' },
      { title: 'Conversion Rate', value: '68%', change: '+3%', icon: Calendar, color: 'text-orange-600' }
    ];

    const Sidebar = () => (
      <div className="w-64 bg-slate-900 text-white h-screen fixed left-0 top-0">
        <div className="p-6">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <Building2 className="w-6 h-6" />
            Nirvaha
          </h1>
        </div>
        <nav className="mt-8">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
            { id: 'customers', label: 'Customers', icon: Users },
            { id: 'deals', label: 'Deals', icon: DollarSign },
            { id: 'calendar', label: 'Calendar', icon: Calendar },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-6 py-3 text-left hover:bg-slate-800 transition-colors ${
                activeTab === item.id ? 'bg-slate-800 border-r-2 border-blue-500' : ''
              }`}
            >
              <item.icon className="w-5 h-5" />
              {item.label}
            </button>
          ))}
        </nav>
        
        <div className="absolute bottom-0 left-0 right-0 p-6">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-2 text-red-400 hover:text-red-300 hover:bg-slate-800 rounded-lg transition-colors"
          >
            <LogOut className="w-5 h-5" />
            Sign Out
          </button>
        </div>
      </div>
    );

    const Header = () => (
      <div className="bg-white shadow-sm border-b px-6 py-4 ml-64">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold capitalize">{activeTab}</h2>
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 transition-colors">
              <Plus className="w-4 h-4" />
              Add New
            </button>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              Welcome, Admin
            </div>
          </div>
        </div>
      </div>
    );

    const StatsGrid = () => (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                <p className="text-2xl font-bold text-gray-900 mt-2">{stat.value}</p>
                <p className="text-sm text-green-600 mt-1">{stat.change} from last month</p>
              </div>
              <div className={`p-3 rounded-full bg-gray-50 ${stat.color}`}>
                <stat.icon className="w-6 h-6" />
              </div>
            </div>
          </div>
        ))}
      </div>
    );

    const CustomerTable = () => (
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6 border-b">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Customers</h3>
            <button className="flex items-center gap-2 text-gray-600 hover:text-gray-900">
              <Filter className="w-4 h-4" />
              Filter
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contact</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {customers.map((customer) => (
                <tr key={customer.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold">
                        {customer.name.charAt(0)}
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{customer.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{customer.company}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900 flex items-center gap-1">
                      <Mail className="w-4 h-4" />
                      {customer.email}
                    </div>
                    <div className="text-sm text-gray-500 flex items-center gap-1">
                      <Phone className="w-4 h-4" />
                      {customer.phone}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      customer.status === 'Active' ? 'bg-green-100 text-green-800' :
                      customer.status === 'Lead' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {customer.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{customer.value}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex items-center gap-2">
                      <button className="text-blue-600 hover:text-blue-900"><Eye className="w-4 h-4" /></button>
                      <button className="text-gray-600 hover:text-gray-900"><Edit className="w-4 h-4" /></button>
                      <button className="text-red-600 hover:text-red-900"><Trash2 className="w-4 h-4" /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );

    const DealsTable = () => (
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">Active Deals</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Deal</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stage</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Probability</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {deals.map((deal) => (
                <tr key={deal.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{deal.title}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{deal.customer}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{deal.value}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      deal.stage === 'Closed Won' ? 'bg-green-100 text-green-800' :
                      deal.stage === 'Negotiation' ? 'bg-blue-100 text-blue-800' :
                      deal.stage === 'Proposal' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {deal.stage}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{deal.probability}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-blue-600 hover:text-blue-900">
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );

    const renderContent = () => {
      switch (activeTab) {
        case 'dashboard':
          return (
            <div>
              <StatsGrid />
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <CustomerTable />
                <DealsTable />
              </div>
            </div>
          );
        case 'customers':
          return <CustomerTable />;
        case 'deals':
          return <DealsTable />;
        case 'calendar':
          return (
            <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
              <Calendar className="w-16 h-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Calendar View</h3>
              <p className="text-gray-600">Calendar integration would go here</p>
            </div>
          );
        default:
          return null;
      }
    };

    return (
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <Header />
        <main className="ml-64 p-6">
          {renderContent()}
        </main>
      </div>
    );
  };

  // Main app render logic
  return isAuthenticated ? <CRMDashboard /> : <LoginPage />;
};

export default CRMApp;