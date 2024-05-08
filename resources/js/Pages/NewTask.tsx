import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import PrimaryButton from '@/Components/PrimaryButton';
import TextInput from '@/Components/TextInput';
import InputLabel from '@/Components/InputLabel';
import { Link } from '@inertiajs/react';
import { Head } from '@inertiajs/react';
import { PageProps } from '@/types';

export default function CreateNewTask({ auth }: PageProps) {
    
    return (
        <AuthenticatedLayout
            user={auth.user}
            header={<h2 className="font-semibold text-xl text-gray-800 leading-tight">Create new task</h2>}
        >
            <Head title="Create new task" />

            <div className="py-12">
                <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
                    <div className="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                        # dnd kit
                        <div className="p-6 text-gray-900">
                            <div className='mb-4'>
                                <InputLabel htmlFor="task_name" value="Task name" />

                                <TextInput
                                    id="task_name"
                                    className="mt-1 block w-1/3"
                                />
                            </div>
                            <div className='mb-4'>
                                <InputLabel htmlFor="task_time" value="Done before" />

                                <TextInput
                                    id="task_time"
                                    className="mt-1 block w-1/3"
                                    type='time'
                                />
                                <TextInput
                                    id="task_date"
                                    className="mt-1 block w-1/3"
                                    value={Date.now()}
                                    type='date'
                                />
                            </div>
                            <div className='mb-4'>
                                <InputLabel htmlFor="task_description" value="Description" />

                                <TextInput
                                    id="task_description"
                                    className="mt-1 block w-1/3"
                                />
                            </div>
                            <Link href={route('dashboard')}>
                                <PrimaryButton className='mb-4'>Create new task</PrimaryButton>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </AuthenticatedLayout>
    );
}
