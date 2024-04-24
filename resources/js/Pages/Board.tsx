import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import PrimaryButton from '@/Components/PrimaryButton';
import { Link } from '@inertiajs/react';
import { Head } from '@inertiajs/react';
import { PageProps } from '@/types';

export default function Board({ auth }: PageProps) {
    
    return (
        <AuthenticatedLayout
            user={auth.user}
            header={<h2 className="font-semibold text-xl text-gray-800 leading-tight">Kanban board</h2>}
        >
            <Head title="Board" />

            <div className="py-12">
                <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
                    <div className="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                        # dnd kit
                        <div className="p-6 text-gray-900">
                            <Link href={route('dashboard')}>
                                <PrimaryButton className='mb-4'>Create new task</PrimaryButton>
                            </Link>
                            <div className='grid gap-6 grid-cols-3'>
                                <div className='bg-slate-200 rounded-md shadow-sm p-2'>
                                    <h2 className='p-2 mb-4 text-center font-semibold tracking-wide text-lg'>To Do</h2>
                                    <ul className='flex flex-col gap-2'>
                                        <li className='bg-gray-50 rounded-md shadow-sm px-2 py-4 cursor-pointer transition ease-in-out hover:bg-gray-100'>
                                            <h2>Úkol 1</h2>
                                        </li>
                                    </ul>
                                </div>
                                <div className='bg-slate-200 rounded-md shadow-sm p-2'>
                                    <h2 className='p-2 mb-4 text-center font-semibold tracking-wide text-lg'>In Progress</h2>
                                    <ul className='flex flex-col gap-2'>
                                        <li className='bg-gray-50 rounded-md shadow-sm px-2 py-4 cursor-pointer transition ease-in-out hover:bg-gray-100'>
                                            <h2>Úkol 1</h2>
                                        </li>
                                    </ul>
                                </div>
                                <div className='bg-slate-200 rounded-md shadow-sm p-2'>
                                    <h2 className='p-2 mb-4 text-center font-semibold tracking-wide text-lg'>Done</h2>
                                    <ul className='flex flex-col gap-2'>
                                        <li className='bg-gray-50 rounded-md shadow-sm px-2 py-4 cursor-pointer transition ease-in-out hover:bg-gray-100'>
                                            <h2>Úkol 1</h2>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </AuthenticatedLayout>
    );
}
